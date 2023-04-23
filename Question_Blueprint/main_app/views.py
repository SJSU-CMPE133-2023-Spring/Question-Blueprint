from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from .forms import AnswerForm
from django.urls import reverse_lazy
from django.contrib import messages
from googleapiclient.discovery import build
API_KEY = 'AIzaSyAAU4tA9zRdw1Mi7aN2YPnQfOWtcJQa3AY' # hopefully no one will use this without our consent

# Create your views here.
def home(request):
    return render(request, 'home.html')

# making a CRUD for question
class QuestionListView(ListView):
    model = Question
    ordering = ["-created_date"]

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            sort_by = self.request.GET.get('sort', '-upvote_num')
            questions = self.model.objects.all()
            if sort_by == 'created_date':
                sorted_questions = questions.order_by('-created_date', '-upvote_num')
            else:
                sorted_questions = questions.order_by('-upvote_num','-created_date')
            context['sorted_questions'] = sorted_questions
            return context


class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    context_object_name = 'single_question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answers = self.object.answer.all()
        sorted_answers = answers.order_by('-upvote_num')
        context['sorted_answers'] = sorted_answers
        return context
    

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    context_object_name = 'single_question'
    fields = ['title', 'content', 'tag']

    def form_valid(self, form):
        form.instance.user = self.request.user
        fields = ['title', 'content', 'tag']
        for part in fields:
            input_text = str(form.cleaned_data.get(part))
            if input_text is not None:
                input_text_encoded = input_text.encode('utf-8')
                violation_key = perspective(input_text_encoded, form)    
                print(violation_key)
                if violation_key:
                    messages.error(self.request, f"Your {part} is violating {violation_key}")
                    return self.form_invalid(form)  # Call form_invalid() to display the error message
        return super().form_valid(form)
    

class QuestionUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView, ):
    model = Question
    fields = ['title', 'content', 'tag']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        fields = ['title', 'content', 'tag']
        for part in fields:
            input_text = str(form.cleaned_data.get(part))
            if input_text is not None:
                input_text_encoded = input_text.encode('utf-8')

                violation_key = perspective(input_text_encoded, form)    
                print(violation_key)
                if violation_key:
                    messages.error(self.request, f"Your {part} is violating {violation_key}")
                    return self.form_invalid(form)  
            return super().form_valid(form)
    
    # prevent people change others' questions
    def test_func(self):
        ques = self.get_object()
        if self.request.user == ques.user:
            return True
        return False
    
    def handle_no_permission(self):
        return render(self.request, 'error.html')

class QuestionDeleteView( UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Question
    context_object_name = 'single_question'
    success_url = '/question/'
    
    def test_func(self):
        ques = self.get_object()
        if self.request.user == ques.user:
            return True
        return False
    
    def handle_no_permission(self):
        return render(self.request, 'error.html')
    

class AnswerDetailView(CreateView):
    model = Answer
    context_object_name = 'ans'
    form_clas = AnswerForm
    template_name = 'main_app/question_detail.html'
    success_url = reverse_lazy('main_app:question_view')
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        field = 'content'

        input_text = str(form.cleaned_data.get(field))
        if input_text is not None:
            input_text_encoded = input_text.encode('utf-8')

            violation_key = perspective(input_text_encoded, form)    
            print(violation_key)
            if violation_key:
                messages.error(self.request, f"Your {field} is violating {violation_key}")
                return self.form_invalid(form)  
        return super().form_valid(form)
    
    def get_queryset(self):
        return Answer.objects.order_by('-created_date')
    

class AnswerAddView(CreateView):

    model = Answer
    ordering = ["-created_date"]
    context_object_name = 'single_question'
    form_class = AnswerForm
    template_name = 'main_app/answer.html'
    
    def get_queryset(self):
        return Answer.objects.order_by('-created_date')

    def form_valid(self, form):
        self.success_url = reverse_lazy('main_app:question_detail_view', args=[self.kwargs['pk']])
        form.instance.question_id = self.kwargs['pk']
        form.instance.user_id = self.request.user.id
        inp = form.cleaned_data.get('content')


        return super().form_valid(form) 





    

def perspective(input_text, form):
    client = build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=API_KEY,
            static_discovery=False
        )

    if input_text is not None:

        analyze_request = {
            'comment': {
                'type': 'PLAIN_TEXT',
                'text': input_text.decode('utf-8')
            },
            'requestedAttributes': {'TOXICITY': {}, 
                                    'SEVERE_TOXICITY': {},
                                    'IDENTITY_ATTACK': {},
                                    'INSULT': {},
                                    'PROFANITY': {},
                                    'THREAT': {},
                                    'SEXUALLY_EXPLICIT': {},
                                    },
            'languages': ['en'],

        }

        fields = ["TOXICITY", "SEVERE_TOXICITY", "IDENTITY_ATTACK", "INSULT", "PROFANITY", "THREAT", "SEXUALLY_EXPLICIT"]
        res = {}

        response = client.comments().analyze(body=analyze_request).execute()

        for field in fields:
            res[field] = response['attributeScores'][field]['summaryScore']['value']
        res = dict(sorted(res.items(), key=lambda item: item[1], reverse=True)) 
        threshold = 0.6
        violation_key = [key for key, value in res.items() if value >= threshold]
        return violation_key