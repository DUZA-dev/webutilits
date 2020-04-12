function deleteFile () {
  $.post(last_function_elem.action, $(last_function_elem).serialize(), function(data) {
    last_function_data = data;
    if ("errors" in data) {
      $('ul.error-list').remove();
      error_list = $('<ul class="error-list"></ul>');
      for (var i = 0; i < data["errors"].length; i++) {
        error_list.append('<li>'+data["errors"][i]+'</li>');
      }
      $(last_function_elem).append(error_list);
    } else {
      $('.blockdownloadfile > form').remove();
      info = $('.blockdownloadfile > p');
      info.css({'font-size': '20px', 'text-decoration': 'underline', 'text-align': 'center', 'background': 'black', 'color': 'white', 'padding': '10px 0'})
      info.text('Файл больше не доступен');
    }
  })
}

function displayConfirmBlock(titleMsg, msg, confirmText, cancelText, functionReturn, e) {
  $('.body-message > .title-message').text(titleMsg);
  $('.body-message > .message').text(msg);
  if (confirmText) {
    var confirm = $('.manipulate-message-menu > .confirm');
    confirm.text(confirmText);
    last_function = functionReturn;
    last_function_elem = e;
    $('.manipulate-message-menu > .confirm').css('display', 'block')
  } else {
    $('.manipulate-message-menu > .confirm').css('display', 'none')
  }

  if (cancelText) {
    $('.manipulate-message-menu > .cancel').text(cancelText);
  }

  $('.main-message').css({'display': 'block'});
}


$('form[name="delete"]').submit(function (e) {
  e.preventDefault();
  displayConfirmBlock(
    'Удаление файла',
    'Вы уверены, что хотите удалить файл?',
    'Да',
    'Нет',
    deleteFile,
    this
  )
})


function download(e) {
  e.preventDefault();
  last_function_elem = this;
  $.post(this.action, $(this).serialize(), function(data) {
    $('ul.error-list').remove();
    last_function_data = data;
    if ("errors" in data) {
      error_list = $('<ul class="error-list"></ul>');
      for (var i = 0; i < data["errors"].length; i++) {
        error_list.append('<li>'+data["errors"][i]+'</li>');
      }
      $(last_function_elem).append(error_list);
    } else {
      $('form[name="download"]').unbind('submit').submit();
      downloadBind();
    }
  })
}

function downloadBind() {
  $('form[name="download"]').bind('submit', download);
}

downloadBind();
