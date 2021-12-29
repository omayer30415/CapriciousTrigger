$(document).ready(function () {
    fetch(('/api/game/wl'))
        .then((response) => response.json())
        .then((result) => {
            if (result.message == 'YOU LOSE') {
                document.querySelectorAll('.us').forEach((us) => {
                    $(us).remove();
                    $('#wl').html('<h1>!| YOU LOSE |!</h1>');
                })
            } else if (result.message == "YOU WIN") {
                document.querySelectorAll('.op').forEach((op) => {
                    $(op).remove();
                    $('#wl').html('<h1>** !! YOU WIN !! **</h1>');
                    $('#next').css('display', 'inline-block');
                })
            }
        })

    // If user selects any of his general
    document.querySelectorAll('.user-generals-photo').forEach((general) => {
        $(general).click(function () {
            document.querySelectorAll('.army').forEach((a) => {
                $(a).removeClass('selected');
                sessionStorage.removeItem('ugn_id')
                sessionStorage.removeItem('usd_id')
            })
            $(general).addClass('selected');
            const g_id = this.dataset.general
            sessionStorage.setItem('ugn_id', g_id)



        });
    })

    // If user selects on any of his soldier
    document.querySelectorAll('.user-soldiers-photo').forEach((soldier) => {
        $(soldier).click(function () {
            document.querySelectorAll('.army').forEach((a) => {
                $(a).removeClass('selected');
                sessionStorage.removeItem('ugn_id')
                sessionStorage.removeItem('usd_id')
            })
            $(soldier).addClass('selected');
            const s_id = this.dataset.soldier
            sessionStorage.setItem('usd_id', s_id)



        });
    })


    // If user targets on any opponent general
    document.querySelectorAll('.op-generals-photo').forEach((op_general) => {
        $(op_general).click(function () {
            if ((sessionStorage.getItem('ugn_id')) != null || (sessionStorage.getItem('usd_id') != null)) {
                document.querySelectorAll('.army').forEach((a) => {
                    sessionStorage.removeItem('df_id')
                })
                const op_general_id = this.dataset.general
                sessionStorage.setItem('df_id', op_general_id)
                const general_id = sessionStorage.getItem('ugn_id')
                const soldier_id = sessionStorage.getItem('usd_id')


                // If the attacker is user's general and defender is opponent general
                if ((sessionStorage.getItem('ugn_id') != null) && (sessionStorage.getItem('usd_id') == null)) {
                    fetch(`/api/game/gg/${general_id}/${op_general_id}`, {
                        method: 'PUT',
                        headers: {
                            'X-CSRFToken': csrftoken
                        }
                    })
                        .then((response1) => response1.json())
                        .then((result1) => {
                            shot_animation(op_general_id, op_general, result1)
                            op_attack()
                        })

                    // If the attacker is user's soldier and defender is opponent general
                } else if ((sessionStorage.getItem('ugn_id') == null) && (sessionStorage.getItem('usd_id') != null)) {
                    fetch(`/api/game/sg/${soldier_id}/${op_general_id}`, {
                        method: 'PUT',
                        headers: {
                            'X-CSRFToken': csrftoken
                        }
                    })
                        .then((response1) => response1.json())
                        .then((result1) => {
                            shot_animation(op_general_id, op_general, result1)
                            op_attack()
                        })
                }
            }
        });
    })


    // If user targets on any opponent soldier
    document.querySelectorAll('.op-soldiers-photo').forEach((op_soldier) => {
        $(op_soldier).click(function () {
            if ((sessionStorage.getItem('ugn_id')) != null || (sessionStorage.getItem('usd_id') != null)) {
                const op_s_id = this.id
                sessionStorage.setItem('df_id', op_s_id)
                const op_soldier_id = sessionStorage.getItem('df_id')
                const general_id = sessionStorage.getItem('ugn_id')
                const soldier_id = sessionStorage.getItem('usd_id')

                // If attacker is user's general and defender is opponent soldier
                if ((sessionStorage.getItem('ugn_id') != null) && (sessionStorage.getItem('usd_id') == null)) {
                    fetch(`/api/game/gs/${general_id}/${op_soldier_id}`, {
                        method: 'PUT',
                        headers: {
                            'X-CSRFToken': csrftoken
                        }
                    })
                        .then((response1) => response1.json())
                        .then((result1) => {
                            shot_animation(op_soldier_id, op_soldier, result1)
                            op_attack()
                        })

                    // If attacker is user's soldier and defender is opponent soldier
                } else {
                    fetch(`/api/game/ss/${soldier_id}/${op_soldier_id}`, {
                        method: 'PUT',
                        headers: {
                            'X-CSRFToken': csrftoken
                        }
                    })
                        .then((response1) => response1.json())
                        .then((result1) => {
                            shot_animation(op_soldier_id, op_soldier, result1)
                            op_attack()
                        })
                }
            }
        })
    });
})


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function shot_animation(def_id, def_element, result1) {
    if (result1.message == 'Miss') {
        $(`#ms${def_id}`).html('Miss');
        $(`#ms${def_id}`).addClass('message');
        $(`#ms${def_id}`).css('animationPlayState', 'running');
        $(`#ms${def_id}`).on('animationend', () => {
            $(`#ms${def_id}`).removeClass('message')
            $(`#ms${def_id}`).html('');
        })
    } else if (result1.message == 'Success') {
        $(`#ms${def_id}`).html('-1');
        $(`#ms${def_id}`).addClass('message');
        $(`#ms${def_id}`).css('animationPlayState', 'running');
        $(`#ms${def_id}`).on('animationend', () => {
            $(`#ms${def_id}`).removeClass('message')
            $(`#ms${def_id}`).html('');
        })
    } else {
        $(`#ms${def_id}`).html('Killed');
        $(`#ms${def_id}`).addClass('message');
        $(`#ms${def_id}`).css('animationPlayState', 'running');
        $(`#ms${def_id}`).on('animationend', () => {
            $(`#ms${def_id}`).removeClass('message')
            $(`#ms${def_id}`).html('');
        })
        $(`#div${def_id}`).addClass('remove');
        $(`#div${def_id}`).css('animationPlayState', 'running')
        $(`#div${def_id}`).on('animationend', () => { $(def_element).css('visibility', 'hidden') })
        if (result1.score_i == 'user') {
            $('#u-score').html(`${result1.score}`);
        } else {
            $('#o-score').html(`${result1.score}`);
        }
        def_element.style.visibility = 'hidden'
    }
}

function op_attack() {
    fetch((`/api/game/random_attack`), {
        method: 'PUT',
        headers: {
            'X-CSRFToken': csrftoken
        }
    }).then((response) => response.json())
        .then((output) => {
            $(`#${output.attacker_id}`).addClass('selected');
            const defender = $(`#${output.defender_id}`)
            shot_animation(`${output.defender_id}`, defender, output)
            $(`#${output.attacker_id}`).removeClass('selected')
        })
    fetch(('/api/game/wl'))
        .then((response) => response.json())
        .then((result) => {
            if (result.message == 'YOU LOSE') {
                document.querySelectorAll('.us').forEach((us) => {
                    $(us).remove();
                    $('#wl').html('<h1>!| YOU LOSE |!</h1>');
                })
            } else if (result.message == "YOU WIN") {
                document.querySelectorAll('.op').forEach((op) => {
                    $(op).remove();
                    $('#wl').html('<h1>** !! YOU WIN !! **</h1>');
                    $('#next').css('display', 'inline-block');
                })
            }
        })
}