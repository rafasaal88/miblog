$(document).ready(function($) {

	$('.card__share > a').on('click', function(e){ 
		e.preventDefault() // prevent default action - hash doesn't appear in url
   		$(this).parent().find( 'div' ).toggleClass( 'card__social--active' );
		$(this).toggleClass('share-expanded');
    });
  
});

$(document).ready(function(){
  $('body').append('<div class="main-mask"></div>')
})
var color = $('.customize').val();
$('input').change(function(){
  var color = $('input').val();
  $('.color').css('background-color','hsl('+color+',100%,40%');
	$('nav ul li ul li').css('background-color','hsl('+color+',100%,40%');
});

// toggle

$('div.toggle').click(function(){
  $(this).toggleClass('active');
  $('nav').toggleClass('active');
  $('.main-mask').fadeToggle(400);
})

// upsize

$('.upsize').click(function(){
  $('.upsize ul').slideToggle(400)
})

//material button animation
 $('.GF-btn').mousedown(function (e) {
    var target = e.target;
    var rect = target.getBoundingClientRect();
    var ripple = target.querySelector('.ripple');
    $(ripple).remove();
    ripple = document.createElement('span');
    ripple.className = 'ripple';
    ripple.style.height = ripple.style.width = Math.max(rect.width, rect.height) + 'px';
    target.appendChild(ripple);
    var top = e.pageY - rect.top - ripple.offsetHeight / 2 -  document.body.scrollTop;
    var left = e.pageX - rect.left - ripple.offsetWidth / 2 - document.body.scrollLeft;
    ripple.style.top = top + 'px';
    ripple.style.left = left + 'px';
    return false;
});
//GF inputs
$('.GF-input-text input').focusout(function(){
    var text_val = $(this).val();
    if(text_val == '') {
        $(this).removeClass('has-value');
    }else {
        $(this).addClass('has-value');
    }
});