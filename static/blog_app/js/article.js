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

const all_pop_article = document.getElementById('p_t_r').innerHTML

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