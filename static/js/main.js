$(document).ready(function() {
	// ***********************for adding tour to wishlist
	const token = '{{csrf_token}}';
	$('#add_to_wislist').on('click', function(event) {
		event.preventDefault();
		console.log('icon clicked!'); // sanity check
		add_product();
	});
	function add_product() {
		console.log('add Product working');
		$.ajax({
			headers: { 'X-CSRFToken': token },
			url: "{% url 'ajaxWishlist' product.id %}",
			type: 'POST',
			success: function(json) {
				if (json.product_added == 'product_added') {
					$().prepend(alert('Product added succefully to your wishlist'));
				} else if (json.already_added == 'already_added') {
					$().prepend(alert('Product already added to your wishlist'));
				}
				console.log('ajax process completed');
			}
		});
	} // end of add tour to wishlist ***********************************
	// ***********************for adding product to cart
	$('#add_to_cart').on('submit', function(event) {
		event.preventDefault();
		console.log('icon clicked!'); // sanity check
		add_item();
	});
	function add_item() {
		$('.closeAlert').empty(); // this line for not repeating the same alert every time the button clicked
		console.log('create post is working!'); // sanity check
		$.ajax({
			url: "{% url 'cart:ajax_add_cart' product.id %}", // the endpoint
			type: 'POST', // http method
			data: {
				update: $('#update').val(),
				quantity: $('#quantity').val()
				// the_rate : $('#post-rate').val(),
			}, // data sent with the post request

			// handle a successful response
			// i used if else statement that after completein the ajax request succefully it may return the response data
			//null from my views.py so it will alert fail massage because this means that review did not saved
			success: function(json) {
				// $().prepend(alert("Item Added To Your Cart"));
				// $('#check_cart').prepend("<a href='{% url 'cart:cart_detail' %}'>Check Your Cart</a>");
				$('.closeAlert').prepend("<a href='{% url 'cart:cart_detail' %}'>Check Your Cart</a>");

				$('#header').load(window.location.href + ' #header'); // reload the navbarcart
			},

			// handle a non-successful response
			error: function(xhr, errmsg, err) {
				$('#results').html(
					"<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " +
						errmsg +
						" <a href='#' class='close'>&times;</a></div>"
				); // add the error to the dom
				console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
			}
		});
	} // end of add tour to cart ***********************************

	// Next code is for csrf :
	$(function() {
		// This function gets cookie with a given name
		function getCookie(name) {
			var cookieValue = null;
			if (document.cookie && document.cookie != '') {
				var cookies = document.cookie.split(';');
				for (var i = 0; i < cookies.length; i++) {
					var cookie = jQuery.trim(cookies[i]);
					// Does this cookie string begin with the name we want?
					if (cookie.substring(0, name.length + 1) == name + '=') {
						cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
						break;
					}
				}
			}
			return cookieValue;
		}
		var csrftoken = getCookie('csrftoken');

		/*
  The functions below will create a header with csrftoken
  */

		function csrfSafeMethod(method) {
			// these HTTP methods do not require CSRF protection
			return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
		}
		function sameOrigin(url) {
			// test that a given url is a same-origin URL
			// url could be relative or scheme relative or absolute
			var host = document.location.host; // host + port
			var protocol = document.location.protocol;
			var sr_origin = '//' + host;
			var origin = protocol + sr_origin;
			// Allow absolute or scheme relative URLs to same origin
			return (
				url == origin ||
				url.slice(0, origin.length + 1) == origin + '/' ||
				(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
				// or any other URL that isn't scheme relative or absolute i.e relative.
				!/^(\/\/|http:|https:).*/.test(url)
			);
		}

		$.ajaxSetup({
			beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
					// Send the token to same-origin, relative URLs only.
					// Send the token only if the method warrants CSRF protection
					// Using the CSRFToken value acquired earlier
					xhr.setRequestHeader('X-CSRFToken', csrftoken);
				}
			}
		});
	}); //End of csrf token
}); //end document.ready
