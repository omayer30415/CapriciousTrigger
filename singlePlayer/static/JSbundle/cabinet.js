$(document).ready(function () {
    document.querySelectorAll('.general_names').forEach((general) => {
        $(general).click(function () {
            general_id = this.dataset.general
            console.log(general_id)
            fetch(`/api/generals/${general_id}`)
                .then((response) => response.json())
                .then((result) => {
                    $('#attributes').empty();
                    $('#attributes').addClass('attr')
                    const img = document.createElement('img')
                    const heading = document.createElement('h3')
                    const ul = document.createElement('ul')
                    const li1 = document.createElement('li')
                    const li2 = document.createElement('li')
                    const li3 = document.createElement('li')
                    const li4 = document.createElement('li')
                    const li5 = document.createElement('li')
                    const li6 = document.createElement('li')
                    const li7 = document.createElement('li')
                    img.src = result.cap_image_url
                    img.alt = `${result.name}'s cap photo`
                    img.className = 'general_image'
                    ul.className = 'general_attributes'
                    $(heading).html('Attributes');
                    $(li1).html(`Name: ${result.name}`);
                    $(li2).html(`Attack: ${result.attack}`);
                    $(li3).html(`Defense: ${result.defense}`);
                    $(li4).html(`Life: ${result.life}`);
                    $(li5).html(`Killed soldiers: ${result.killed_units}`);
                    $(li7).html(`Cap image URL: ${result.cap_image_url}`);
                    $(li7).addClass('url');
                    if (result.leading_role) {
                        $(li6).html('Leading Role: Yes');
                    } else {
                        $(li6).html('Leading Role: No');
                    }
                    $('#attributes').append(img);
                    $('#attributes').append(heading);
                    $('#attributes').append(ul);
                    $(ul).append(li1);
                    $(ul).append(li2);
                    $(ul).append(li3);
                    $(ul).append(li4);
                    $(ul).append(li5);
                    $(ul).append(li6);

                })
        });
    })
    fetch((`/current_user`))
        .then((response) => response.json())
        .then((user) => sessionStorage.setItem('user', JSON.stringify(user.username)))
    document.querySelectorAll('.promote').forEach((soldier) => {
        $(soldier).click(function () {
            let soldier_id = this.dataset.promote
            console.log(soldier_id)
            document.querySelector(`#fr${soldier_id}`).style.display = 'block'
            $(this).hide()
            $(`#promote${soldier_id}`).click(function () {
                fetch(`/api/promote/${soldier_id}`, {
                    method: "POST",
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json; charset=UTF-8',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({
                        soldier_name: $(`#name${soldier_id}`).val(),
                        killed_units: $(`#hd${soldier_id}`).val(),
                        cap_image_url: $(`#cap${soldier_id}`).val(),
                        user: JSON.parse(sessionStorage.getItem('user'))
                    })
                }).then((response) => response.json())
                    .then((result) => {
                        const li = document.createElement('li')
                        li.className = 'general_names'
                        li.dataset.general = `${result.id}`
                        li.innerHTML = result.name
                        $('#generals').append(li);
                        $(`${soldier}`).remove();
                        $(`#sd${soldier_id}`).remove();
                    })
            });
        });
    })
});


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

