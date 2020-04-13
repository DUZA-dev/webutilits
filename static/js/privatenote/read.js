function read(e) {
  e.preventDefault();
  $.post(this.action, $(this).serialize(), function(data) {
    $('ul.error-list').remove();
    if ("errors" in data) {
      error_list = $('<ul class="error-list"></ul>');
      for (var i = 0; i < data["errors"].length; i++) {
        error_list.append('<li>'+data["errors"][i]+'</li>');
      }
      $(this).append(error_list);
    } else {
      $('form[name="readNote"]').remove();
      $('div.note-main').append('<div class="note">' + data['note'] + '<div class="pub_date"><b>Опубликовано: </b>' + data['pub_date'] + '</div></div>');
    }
  })
}

$('form[name="readNote"]').bind('submit', read);
