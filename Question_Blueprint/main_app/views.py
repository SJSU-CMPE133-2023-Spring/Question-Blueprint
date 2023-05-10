from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Question, QuestionUpvote, Answer, AnswerUpvote
from .forms import AnswerForm
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from googleapiclient.discovery import build
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .funcs import preprocess_questions, similarity_check
from django.db.models import Q, Count


from gtts import gTTS
from tempfile import TemporaryFile


# Create your views here.
def home(request):
    return render(request, 'home.html')

# making a CRUD for question


class QuestionListView(ListView):
    model = Question
    ordering = ['-created_date']
    template_name = 'main_app/question_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = self.model.objects.all()
        sort_by = self.request.GET.get('sort', '-upvote_num')
        if sort_by == 'created_date':
            sorted_questions = questions.order_by(
                '-created_date', '-upvote_num')
        else:
            sorted_questions = questions.order_by(
                '-upvote_num', '-created_date')
        paginator = Paginator(sorted_questions, 4)  # 3 questions per page
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context['sorted_questions'] = page_obj
        return context


# TO-DO answer sort will be going into here
class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    context_object_name = 'single_question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answers = self.object.answer.all()

        sort_by = self.request.GET.get('sort', '-upvote_num')
        if sort_by == 'created_date':
            sorted_answers = answers.order_by('-created_date', '-upvote_num')
        else:
            sorted_answers = answers.order_by('-upvote_num', '-created_date')

        context['sorted_answers'] = sorted_answers

        cur_id = kwargs.get('object').id
        cur_question = Question.objects.get(id=cur_id)

        questions = Question.objects.exclude(id=cur_id)
        question_list = preprocess_questions(questions)

        sim_ques = similarity_check(cur_question, question_list)
        print(sim_ques)

        if sim_ques:

            sim_id = sim_ques[0]
            sim_question_title = Question.objects.get(id=sim_id).title

            context['sim_id'] = sim_id
            context['sim_quesiton_title'] = sim_question_title

        context['sim_ques'] = sim_ques
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
                    messages.error(
                        self.request, f"In order to proceed, you need to modify your {part} since it has breached the {violation_key} guideline.")
                    # Call form_invalid() to display the error message
                    return self.form_invalid(form)

        res = super().form_valid(form)
        question_id = form.instance.id
        question = get_object_or_404(Question, id=question_id)
        save_audio_file(question, question.content)
        return res

    def get_success_url(self):
        question_id = self.object.id  # Get the ID of the question that was just created
        return reverse('main_app:question_detail_view', kwargs={'pk': question_id})


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
                    messages.error(
                        self.request, f"In order to proceed, you need to modify your {part} since it has breached the {violation_key} guideline.")
                    # Call form_invalid() to display the error message
                    return self.form_invalid(form)

        res = super().form_valid(form)
        question_id = form.instance.id
        question = get_object_or_404(Question, id=question_id)
        save_audio_file(question, question.content)
        return res

    # prevent people change others' questions
    def test_func(self):
        ques = self.get_object()
        if self.request.user == ques.user:
            return True
        return False

    def handle_no_permission(self):
        return render(self.request, 'error.html')

    def get_success_url(self):
        question_id = self.object.id  # Get the ID of the question that was just created
        return reverse('main_app:question_detail_view', kwargs={'pk': question_id})


class QuestionDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
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


class AnswerAddView(CreateView):

    model = Answer
    form_class = AnswerForm
    template_name = 'main_app/answer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        single_question = get_object_or_404(Question, id=self.kwargs['pk'])
        print(single_question)
        context['single_question'] = single_question
        return context

    def get_queryset(self):
        return Answer.objects.order_by('-created_date')

    def form_valid(self, form):
        self.success_url = reverse_lazy(
            'main_app:question_detail_view', args=[self.kwargs['pk']])
        form.instance.question_id = self.kwargs['pk']
        form.instance.user_id = self.request.user.id
        inp = form.cleaned_data.get('content')
        violation_key = None

        input_text = str(inp)
        if input_text is not None and contains_alphabet(input_text):
            input_text_encoded = input_text.encode('utf-8')
            violation_key = perspective(input_text_encoded, form)
            print(violation_key)

        if violation_key:
            messages.error(
                self.request, f"In order to proceed, you need to modify your answer since it has breached the {violation_key} guideline.")
            return self.form_invalid(form)
        return super().form_valid(form)


# function to analyze and classify whether the text is vulgar, toxic,... or valid
def perspective(input_text, form):
    client = build(
        "commentanalyzer",
        "v1alpha1",
        developerKey='AIzaSyAAU4tA9zRdw1Mi7aN2YPnQfOWtcJQa3AY',
        static_discovery=False
    )

    try:
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

            fields = ["TOXICITY", "SEVERE_TOXICITY", "IDENTITY_ATTACK",
                      "INSULT", "PROFANITY", "THREAT", "SEXUALLY_EXPLICIT"]
            res = {}

            response = client.comments().analyze(body=analyze_request).execute()

            for field in fields:
                res[field] = response['attributeScores'][field]['summaryScore']['value']
            res = dict(
                sorted(res.items(), key=lambda item: item[1], reverse=True))
            print(res)
            threshold = 0.6
            violation_key = [key for key,
                             value in res.items() if value >= threshold]
            return violation_key
    except:
        return None

# function convert text to speech by gTTS library


def save_audio_file(question, text):
    if not contains_alphabet(text):
        text = "None"

    tts = gTTS(text)
    with TemporaryFile() as f:
        tts.write_to_fp(f)

        f.seek(0)

        file_name = str(question.id) + ".mp3"
        question.audio_file.save(file_name, f)


def contains_alphabet(input_string):
    for char in input_string:
        if char.isalpha():
            return True
    return False


@login_required
def upvote(request, pk):

    if request.method == "POST":
        vote_type = request.POST.get("vote_type")
        if vote_type == "question":
            question = get_object_or_404(Question, id=pk)
            upvote = QuestionUpvote.objects.filter(
                question=question, user=request.user).first()
            if upvote:
                upvote.delete()
            else:
                QuestionUpvote.objects.create(
                    question=question, user=request.user)
                print(f"Question Upvote success")

        if vote_type == "answer":
            ans_id = request.POST.get('ans_id')
            answer = get_object_or_404(Answer, id=ans_id)
            upvote = AnswerUpvote.objects.filter(
                answer=answer, user=request.user).first()
            if upvote:
                upvote.delete()
            else:
                AnswerUpvote.objects.create(answer=answer, user=request.user)

                print(f"Answer Upvote success")
        return redirect('main_app:question_detail_view', pk)


# Search
def search(request):
    query = request.GET.get('q')
    if query:
        results = Question.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query))

        if results:
            return render(request, 'main_app/search.html', {'results': results})

    return render(request, 'main_app/not_found_page.html')
