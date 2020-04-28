// 전문분야 자동 선택

function specialty_checked() {

    var merged_specialty = document.querySelector("#merged_specialty");
    var specialtyList = merged_specialty.value.split('/');
    form = document.querySelector("#specialty_form");

    form.querySelectorAll("input[name='fields']").forEach(el => {
        if (specialtyList.includes(el.value))
            el.setAttribute('checked', 'checked');
    })

}

specialty_checked();