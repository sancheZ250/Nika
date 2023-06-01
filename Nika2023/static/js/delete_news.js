$(document).ready(function() {
    $('.delete-news-btn').on('click', function() {
        var csrftoken = Cookies.get('csrftoken');
        var newsId = $(this).data('news-id');
        var $newsCard = $(this).closest('.card')
        $.ajax({
            url: '/News/delete/' + newsId + '/',
            type: 'POST',
            data: {},
            beforeSend: function(xhr, settings) {
                // Добавление CSRF-токена в заголовок запроса
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            success: function(response) {
                // Обработка успешного удаления новости
                // Например, можно обновить список новостей или выполнить другие действия
                $newsCard.remove();
            },
            error: function(xhr, ajaxOptions, thrownError) {
            }
        });
    });
});





