

$(document).ready(
  function() {
    if ($('ul.menu').css('display')!='none' && window.width <= 866) {
      $('ul.menu').css('display', 'none');
    }
  }
);

$('.toggle[for="drop"]').click(function () {
  if ($('ul.menu').css('display')=='none') {
    $('nav').css({'height': '100%'});
    $('body').css({'overflow': 'hidden'})
  } else {
    $('nav').css({'height': 'auto'});
    $('body').css({'overflow-y': 'visible'})
  }
})
