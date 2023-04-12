// ////////////////////////////////  ///// JQuery \\\\\ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ \\
// /////////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ \\
// /////////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ \\

$(document).ready(function() {
	$('#id_username').change(function() {
		console.log($(this).val());
		var username = $(this).val();

		$.ajax({
			url: 'ajax/validate_username',
			data: {
				username: username
			},
			dataType: 'json',
			success: function(data) {
				if (data.is_taken) {
					alert(data.error_message);
				}
			}
		});
	});

	$('#email').change(function() {
		var email = $(this).val();

		$.ajax({
			url: 'ajax/validate_email',
			data: {
				email: email
			},
			dataType: 'json',
			success: function(data) {
				if (data.is_taken) {
					alert(data.error_message);
				}
			}
		});
	});
});

/////   >>>>>>>>>>>>>>>>>>>>>>  Daily Tours validators
// $(document).ready(function() {
// 	$('#date').change(function() {
// 		console.log($(this).val());
// 		var date = $(this).val();

// 		$.ajax({
// 			url: 'ajax/validate_daily_tours_date',
// 			data: {
// 				date: date
// 			},
// 			dataType: 'json',
// 			success: function(data) {
// 				if (data.NA) {
// 					alert(data.error_message);
// 				}
// 			}
// 		});
// 	});

/////   >>>>>>>>>>>>>>>>>>>>>>  End Daily Tours validators

// ////////////////////////////////  Vanilla JavaScript \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ \\
// /////////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ \\
// /////////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ \\

//--------------------------------
// This code compares two fields in a form and submit it
// if they're the same, or not if they're different.
//--------------------------------
function checkEmail() {
	const EMAIL_1 = document.getElementById('EMAIL_1');
	const EMAIL_2 = document.getElementById('EMAIL_2');
	if (EMAIL_1.value != EMAIL_2.value) {
		// alert('Two emails don\'t match!');
		document.getElementById('email_err').innerHTML = "Two emails don't match!";
		return false;
	}
	if (EMAIL_1.value == EMAIL_2.value) {
		document.getElementById('email_err').innerHTML = '';
	}
}

// Owl Carousel //

$('.owl-carousel1').owlCarousel({
	items: 1,
	nav: false,
	dots: false,
	loop: true,

	autoplay: true,
	autoplayTimeout: 5000,
	animateOut: 'fadeOut'
});

$('.owl-carousel2').owlCarousel({
	items: 1,
	nav: true,
	dots: false,
	loop: true,
	autoplay: true,
	autoplayTimeout: 5000
});

$('.owl-carousel3').owlCarousel({
	items: 4,
	nav: true,
	dots: false,
	loop: true,
	margin: 20,
	merge: true,
	autoplay: true,
	autoplayTimeout: 5000,
	responsive: {
		0: {
			items: 2,
			nav: true
		},
		600: {
			items: 3,
			nav: false
		},
		1000: {
			items: 4,
			nav: true
		}
	}
});

$('.owl-carousel5').owlCarousel({
	items: 1,
	nav: false,
	dots: true,
	loop: true,

	autoplay: true,
	autoplayTimeout: 5000,
	animateOut: 'fadeOut'
});

$('.owl-carousel6').owlCarousel({
	items: 1,
	nav: true,
	dots: false,
	loop: true,
	margin: 50,
	merge: true,

	autoplayTimeout: 5000,
	responsive: {
		0: {
			items: 1,
			nav: true
		},
		600: {
			items: 2,
			nav: false
		},
		1000: {
			items: 3,
			nav: true
		}
	}
});

//testmonial slideshow

$('.owl-carousel7').owlCarousel({
	items: 1,
	nav: true,
	dots: false,
	loop: true,
	margin: 50,
	merge: true,
	autoplay: true,
	autoplayTimeout: 5000,
	navText: [
		'<i class="fa fa-angle-left" aria-hidden="true"></i>',
		'<i class="fa fa-angle-right" aria-hidden="true"></i>'
	],
	navContainer: '.main-content .custom-nav',
	responsive: {
		0: {
			items: 1,
			nav: true
		},
		600: {
			items: 1,
			nav: false
		},
		1000: {
			items: 1,
			nav: true
		}
	}
});

//test owl
$(document).ready(function() {
	var bigimage = $('#big');
	var thumbs = $('#thumbs');
	//var totalslides = 10;
	var syncedSecondary = true;

	bigimage
		.owlCarousel({
			items: 1,
			slideSpeed: 5000,
			nav: true,
			autoplay: true,
			dots: false,
			loop: true,
			responsiveRefreshRate: 200,
			navText: [
				'<i class="fa fa-arrow-left" aria-hidden="true" style="color: white;"></i>',
				'<i class="fa fa-arrow-right" aria-hidden="true" style="color: white;"></i>'
			]
		})
		.on('changed.owl.carousel', syncPosition);

	thumbs
		.on('initialized.owl.carousel', function() {
			thumbs.find('.owl-item').eq(0).addClass('current');
		})
		.owlCarousel({
			items: 4,
			dots: false,
			nav: true,
			navText: [
				'<i class="fa fa-arrow-left" aria-hidden="true" style="color: white;"></i>',
				'<i class="fa fa-arrow-right" aria-hidden="true" style="color: white;"></i>'
			],
			smartSpeed: 200,
			slideSpeed: 2000,
			slideBy: 4,
			responsiveRefreshRate: 100
		})
		.on('changed.owl.carousel', syncPosition2);

	function syncPosition(el) {
		//if loop is set to false, then you have to uncomment the next line
		//var current = el.item.index;

		//to disable loop, comment this block
		var count = el.item.count - 1;
		var current = Math.round(el.item.index - el.item.count / 2 - 0.5);

		if (current < 0) {
			current = count;
		}
		if (current > count) {
			current = 0;
		}
		//to this
		thumbs.find('.owl-item').removeClass('current').eq(current).addClass('current');
		var onscreen = thumbs.find('.owl-item.active').length - 1;
		var start = thumbs.find('.owl-item.active').first().index();
		var end = thumbs.find('.owl-item.active').last().index();

		if (current > end) {
			thumbs.data('owl.carousel').to(current, 100, true);
		}
		if (current < start) {
			thumbs.data('owl.carousel').to(current - onscreen, 100, true);
		}
	}

	function syncPosition2(el) {
		if (syncedSecondary) {
			var number = el.item.index;
			bigimage.data('owl.carousel').to(number, 100, true);
		}
	}

	thumbs.on('click', '.owl-item', function(e) {
		e.preventDefault();
		var number = $(this).index();
		bigimage.data('owl.carousel').to(number, 300, true);
	});
});

// End Owl Carousel //

// End Owl Carousel //

//shrink navbar
$(document).ready(function() {
	$(window).on('scroll', function() {
		if ($(window).scrollTop() >= 20) {
			$('.navbar').addClass('compressed');
			$('.logo').addClass('logo-co');
		} else {
			$('.navbar').removeClass('compressed');
			$('.logo').removeClass('logo-co');
		}
	});
});

//open small navbar
$(document).ready(function() {
	$('#bar').click(function() {
		$('#small').slideToggle('slow');
	});
});
//open small navbar-->

$(document).ready(function() {
	$('.zhover').hover(function() {
		$('.zoom').animate({
			width: '200%'
		});
	});
});
//  End open Small Navbar //

// Owl For tour Details

$(document).ready(function() {
	var sync1 = $('#sync1');
	var sync2 = $('#sync2');

	sync1.owlCarousel({
		singleItem: true,
		autoPlay: true,
		slideSpeed: 2000,
		navigation: false,
		pagination: false,
		afterAction: syncPosition,
		responsiveRefreshRate: 200
	});

	sync2.owlCarousel({
		items: 5,
		itemsDesktop: [ 1199, 5 ],
		itemsDesktopSmall: [ 979, 5 ],
		itemsTablet: [ 768, 4 ],
		itemsMobile: [ 479, 4 ],
		pagination: false,
		responsiveRefreshRate: 100,
		afterInit: function(el) {
			el.find('.owl-item').eq(0).addClass('synced');
		}
	});

	function syncPosition(el) {
		var current = this.currentItem;
		$('#sync2').find('.owl-item').removeClass('synced').eq(current).addClass('synced');
		if ($('#sync2').data('owlCarousel') !== undefined) {
			center(current);
		}
	}

	$('#sync2').on('click', '.owl-item', function(e) {
		e.preventDefault();
		var number = $(this).data('owlItem');
		sync1.trigger('owl.goTo', number);
	});

	function center(number) {
		var sync2visible = sync2.data('owlCarousel').owl.visibleItems;
		var num = number;
		var found = false;
		for (var i in sync2visible) {
			if (num === sync2visible[i]) {
				var found = true;
			}
		}

		if (found === false) {
			if (num > sync2visible[sync2visible.length - 1]) {
				sync2.trigger('owl.goTo', num - sync2visible.length + 2);
			} else {
				if (num - 1 === -1) {
					num = 0;
				}
				sync2.trigger('owl.goTo', num);
			}
		} else if (num === sync2visible[sync2visible.length - 1]) {
			sync2.trigger('owl.goTo', sync2visible[1]);
		} else if (num === sync2visible[0]) {
			sync2.trigger('owl.goTo', num - 1);
		}
	}
});
// End Owl For tour Details

// for currency selection
$(document).ready(function() {
	$(function() {
		var genderValue = localStorage.getItem('genderValue');
		if (genderValue != null) {
			$('select[name=currency]').val(genderValue);
		}

		$('select[name=currency]').on('change', function() {
			localStorage.setItem('genderValue', $(this).val());
		});
	});
});
