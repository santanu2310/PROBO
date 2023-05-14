let slideIndex = 0;
showSlides();

const all_pop_article = document.getElementById('p_t_r').innerHTML

function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// function to open close mobile v nav

function navOpen() {
	document.getElementById('nav-link-mob').classList.remove('hide')
}
function navClose() {
	document.getElementById('nav-link-mob').classList.add('hide')
}


// // copied form w3 school for the top slide show
function showSlides() {
	let i;
	let slides = document.getElementsByClassName("banner_1--Slides");
	let dots = document.getElementsByClassName("dot");
	for (i = 0; i < slides.length; i++) {
		slides[i].style.display = "none";
	}
	slideIndex++;
	if (slideIndex > slides.length) { slideIndex = 1 }
	for (i = 0; i < dots.length; i++) {
		dots[i].className = dots[i].className.replace(" active", "");
	}
	slides[slideIndex - 1].style.display = "block";
	dots[slideIndex - 1].className += " active";
	setTimeout(showSlides, 6000);  //6000 is in ms for slide change
}

// send email through fetch api for subscribtion
function subscribe() {
	var emailId = document.getElementById('email').value
	if (emailId != '') {
		const url = window.location.href
		fetch(url, {
			method: 'POST',
			headers: {
				'Content-type': 'application/json',
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify({ 'email': emailId, })
		})
			.then((response) => {
				return response.json()
			})
			.then((data) => {
				console.log(data['status'])
				document.getElementById('email').value = ''
				document.getElementById('email').blur()

				let message
				let alert_class

				if (data['status'] == 'E_Email') {
					message = 'This email address already exist!'
					alert_class = 'exist'
				} else if (data['status'] == 'Success') {
					message = 'Successfully subscribed '
					alert_class = 'success'
				} else if (data['status'] == 'P_Email') {
					message = 'Please entrer a valid email!! '
					alert_class = 'red'
				} else {
					message = 'error : 500 '
					alert_class = 'red'
				}

				let message_box = document.createElement('div')
				message_box.classList.add('message--box', alert_class)
				message_box.innerHTML += `
          <p class="message">${message}</p>
          <button onclick="this.parentElement.remove();">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
            <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
            </svg>
          </button>
        `
				document.getElementById('message--area').appendChild(message_box)

				setTimeout(() => {
					message_box.remove()
				}, 5000)  //remove the alert after 5s.
			})
	}
	else {
		console.log('empty')
	}
}


//

function getBlogs(element,category,section) {
    const url = 'http://127.0.0.1:8000/getblog'
    fetch(url,{
        method: "POST",
        headers : {
            'Content-type': 'application/json',
			'X-CSRFToken': csrftoken
        },
        body : JSON.stringify({'category':category,'section':section})
    })
    .then((response)=>{
        return response.json()
    })
    .then((data) =>{
		let info =JSON.parse(data)
		document.getElementById('p_t_r').innerHTML = ''

		let cat_links = document.getElementsByClassName('popcat')
		for (var i = 0; i < cat_links.length; i++) {
			cat_links[i].classList.remove('focus_element');
		 }
		element.classList.add('focus_element')

		for (obj of info){
			let article_card = document.createElement('div')
			article_card.classList.add('article_card')
			if(obj.fields.short_desc.length > 100) short_desc = obj.fields.short_desc.substring(0,100)

			article_card.innerHTML = `
			<span class="article_card--category">${category}</span>
            <div class="article_card--image">
                <img src="${obj.fields.cover_image}" alt="">
            </div>
            <span class="article_card--date">${obj.fields.date}</span>
            <a href="/article/${obj.pk}" class="article_card--topic">${obj.fields.name}</a>
            <p class="article_card--description">
                ${short_desc}
            </p>
			`
			document.getElementById('p_t_r').appendChild(article_card)


		}
		
    })
}

function allPop(element){
	let cat_links = document.getElementsByClassName('popcat')
		for (var i = 0; i < cat_links.length; i++) {
			cat_links[i].classList.remove('focus_element');
		 }
		element.classList.add('focus_element')
	document.getElementById('p_t_r').innerHTML = all_pop_article
}