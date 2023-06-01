
function hideNewsList() {
  var newsList = document.getElementById("list_of_news");
  if (newsList) {
    newsList.style.display = "none";
  }
}

$(document).ready(function() {
  var searchForm = $('#search-form');
  var searchInput = $('#search-input');
  var searchResults = $('#search-results');

  function performSearch() {
    var searchTerm = searchInput.val();

    var deferred = $.Deferred();

    $.ajax({
      url: 'search/',
      method: 'GET',
      data: { q: searchTerm },
      success: function(response) {
        deferred.resolve(response);
        hideNewsList();
      },
      error: function(jqXHR, textStatus, errorThrown) {
        deferred.reject(errorThrown);
      }
    });

    return deferred.promise();
  }

  searchForm.on('submit', function(e) {
    e.preventDefault();
    searchResults.empty();

    var promise = performSearch();

    promise.done(function(response) {
      searchResults.html(response);
    });

    promise.fail(function(error) {
      console.error('Произошла ошибка:', error);
    });

    promise.always(function() {
      console.log('Запрос выполнен');
    });
  });
});