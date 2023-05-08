// console.log('Connected Successfully')

function search() {
  // Get the search input element
  let input = document.querySelector("#search-input");

  // Get the list of items to search through
  let items = document.querySelectorAll(".searchable");

  // Get the search results element
  let results = document.querySelector("#search-results");

  // Add an event listener to the input element
  input.addEventListener("input", function () {
    // Get the user's search query
    let query = input.value.trim().toLowerCase();

    // Loop through the items and hide/show them based on the search query
    let matchingItems = [];
    for (let i = 0; i < items.length; i++) {
      let item = items[i];
      let text = item.textContent.trim().toLowerCase();
      let match = text.includes(query);

      if (match) {
        item.classList.remove("d-none");
        matchingItems.push(item);
      } else {
        item.classList.add("d-none");
      }
    }

    // Show the search results if the user is actively searching
    if (query.length > 0) {
      let html = "";
      for (let i = 0; i < matchingItems.length; i++) {
        let item = matchingItems[i];
        let text = item.textContent.trim();
        html += "<div>" + text + "</div>";
      }
      results.innerHTML = html;
      results.classList.remove("d-none");
    } else {
      results.innerHTML = "";
      results.classList.add("d-none");
    }
  });
}

// Call the search function to initialize it
search();
