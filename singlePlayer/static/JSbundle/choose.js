document.addEventListener('DOMContentLoaded', function () {
    $('#c_instr').click(function () {
        $('#choose_instr').css('display', 'inline-block');
        $(this).hide();
        $('#close_instr').click(function () {
            $('#choose_instr').hide()
            $('#c_instr').css('display', 'inline-block')
        });

    });

    // See the generals or hide generals list 
    document.querySelectorAll('.see').forEach((see) => {
        $(see).click(function () {
            team_id = this.dataset.team
            const ul = document.querySelector(`#ul${team_id}`)
            ul.style.display = 'block'
            this.style.opacity = 0
            const bt = document.createElement('button')
            bt.className = 'btn btn-warning hid'
            bt.innerHTML = 'Hide'
            $(`#sp${team_id}`).append(bt);
            $(bt).click(function () {
                $(this).hide()
                $(ul).hide();
                see.style.opacity = 1
            });
        });
    })

    // Taking a team and its generals
    document.querySelectorAll('.take').forEach((take) => {
        $(take).click(function () {
            team_id = this.dataset.take
            fetch(`/new_choose/${team_id}`)
                .then((response) => response.json())
                .then((result) => {
                    document.querySelector('#generals_cabinet').style.display = 'block'
                    document.querySelector('#choose').style.display = 'none'
                    result.forEach((general) => {
                        const li = document.createElement('li')
                        li.innerHTML = general.name
                        li.className = 'general_names'
                        $('#generals').append(li);
                    })
                })

        });

    });

})
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
}