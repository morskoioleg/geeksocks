var previous_st=0;
var timer=0;
$(window).scroll(function (event) {
    var st = $(this).scrollTop();
    if (st>=710) {
		if (timer==0){
			timer=setInterval(checkIfNeedSuperman, 1500);
		}
    }
});


function checkIfNeedSuperman(){
	var st = $(this).scrollTop();
	if (previous_st==st)
		flySuperman2();
	previous_st=st;
}

function flySuperman(){
	console.log("FLY");
	clearInterval(timer);
	$('#superman').css('display','block');
	$('#superman').css('right',1);
	$('#superman').css('top',$(this).scrollTop()+($( window ).height()*0.65));
	$('#superman img').css('width',$( window ).width()/3);
	$('#superman').css('width',$( window ).width()/3);
	$('#superman').css('left','auto');
	$('#superman').animate({left: '-250',top: $(this).scrollTop()}, 2000,"linear");
	yaCounter39819550.reachGoal('Fly');
}

function flySuperman2(){
	console.log("FLY2");
	clearInterval(timer);
	$('#superman').css('display','block');
	$('#superman').css('right',0);
	$('#superman').css('top',$(this).scrollTop()+($( window ).height()*0.65));
	$('#superman img').css('width',$( window ).width()/3);
	$('#superman').css('width',$( window ).width()/3);
	$('#superman').animate({right: $( window ).width()*1.1,top: $(this).scrollTop()}, 2000,"easeInBack");
	yaCounter39819550.reachGoal('Fly');
}