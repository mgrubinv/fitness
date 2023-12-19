async function deletWorkoutExercise(exercise_id) {

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    let dataReply = await fetch(`/delete-workout-exercise/${exercise_id}`, {
        method: 'PUT',
        headers: { 'X-CSRFToken': csrftoken },
        mode: 'same-origin',
        body: JSON.stringify({
            delete_exercise: "true"
        })
    }).then(response => response.json()).then(data => { return data }).catch(err => console.log(err));

    var exercise_list = document.querySelector('#workout-exercise-list');
    delete_ex = document.querySelector(`#${dataReply["deleted"]}`);
    exercise_list.removeChild(delete_ex);

    for (var key in dataReply["update"]) {
        document.querySelector(`#${dataReply["update"][key]}`).childNodes[3].innerHTML = key;
    };

};

async function moveUpWorkoutExercise(exercise_id) {

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    let dataReply = await fetch(`/move-up-workout-exercise/${exercise_id}`, {
        method: 'PUT',
        headers: { 'X-CSRFToken': csrftoken },
        mode: 'same-origin',
        body: JSON.stringify({
            move_up: "true"
        })
    }).then(response => response.json()).then(data => { return data }).catch(err => console.log(err));

    if (dataReply["moved"] == "true") {

        document.querySelector(`#${dataReply["moved_down_ex"]}`).childNodes[3].innerHTML = dataReply["moved_down_seq"];
        document.querySelector(`#${dataReply["moved_up_ex"]}`).childNodes[3].innerHTML = dataReply["moved_up_seq"];

        var exercise_list = document.querySelector('#workout-exercise-list');

        var moved_down_text = document.querySelector('#workout-exercise-list').childNodes[((dataReply["moved_up_seq"] * 2) - 2)];
        var moved_down_child = document.querySelector('#workout-exercise-list').childNodes[((dataReply["moved_up_seq"] * 2) - 1)];

        var moved_up_text = document.querySelector('#workout-exercise-list').childNodes[((dataReply["moved_down_seq"] * 2) - 2)];
        var moved_up_child = document.querySelector('#workout-exercise-list').childNodes[((dataReply["moved_down_seq"] * 2) - 1)];

        exercise_list.removeChild(moved_up_text);
        exercise_list.removeChild(moved_up_child);
        exercise_list.insertBefore(moved_up_text, moved_down_text);
        exercise_list.insertBefore(moved_up_child, moved_up_text);
    };

    document.querySelectorAll('#arrow-down-icon').forEach(element => {

        element.onclick = function () {
            moveDownWorkoutExercise(this.dataset.exercise);
        };
    });
};


async function moveDownWorkoutExercise(exercise_id) {

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    let dataReply = await fetch(`/move-down-workout-exercise/${exercise_id}`, {
        method: 'PUT',
        headers: { 'X-CSRFToken': csrftoken },
        mode: 'same-origin',
        body: JSON.stringify({
            move_down: "true"
        })
    }).then(response => response.json()).then(data => { return data }).catch(err => console.log(err));

    if (dataReply["moved"] == "true") {

        document.querySelector(`#${dataReply["moved_down_ex"]}`).childNodes[3].innerHTML = dataReply["moved_down_seq"];
        document.querySelector(`#${dataReply["moved_up_ex"]}`).childNodes[3].innerHTML = dataReply["moved_up_seq"];

        var exercise_list = document.querySelector('#workout-exercise-list');

        var moved_down_text = document.querySelector('#workout-exercise-list').childNodes[((dataReply["moved_up_seq"] * 2) - 2)];
        var moved_down_child = document.querySelector('#workout-exercise-list').childNodes[((dataReply["moved_up_seq"] * 2) - 1)];

        var moved_up_text = document.querySelector('#workout-exercise-list').childNodes[((dataReply["moved_down_seq"] * 2) - 2)];
        var moved_up_child = document.querySelector('#workout-exercise-list').childNodes[((dataReply["moved_down_seq"] * 2) - 1)];

        exercise_list.removeChild(moved_up_text);
        exercise_list.removeChild(moved_up_child);
        exercise_list.insertBefore(moved_up_text, moved_down_text);
        exercise_list.insertBefore(moved_up_child, moved_up_text);
    };

    document.querySelectorAll('#arrow-down-icon').forEach(element => {

        element.onclick = function () {
            moveDownWorkoutExercise(this.dataset.exercise);
        };
    });
};


async function fetchUpdateWorkoutSet(exercise_id, updates) {

    console.log(exercise_id)
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    let dataReply = await fetch(`/update-workout-sets/${exercise_id}`, {
        method: 'PUT',
        headers: { 'X-CSRFToken': csrftoken },
        mode: 'same-origin',
        body: JSON.stringify(updates)
    }).then(response => response.json()).then(data => { return data }).catch(err => console.log(err));

    return dataReply;

};

async function fetchAddSet(exercise_id, new_set) {

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    let dataReply = await fetch(`/add-workout-set/${exercise_id}`, {
        method: 'PUT',
        headers: { 'X-CSRFToken': csrftoken },
        mode: 'same-origin',
        body: JSON.stringify(new_set)
    }).then(response => response.json()).then(data => { return data }).catch(err => console.log(err));

    return dataReply;


};

function renderUpdatedWorkoutSets(exercise_id, dataReply) {
    
    let mod_exercise = document.querySelector(`tr#workout-exercise-${exercise_id}`);
    let table_stats_form = mod_exercise.querySelector('table#stats-form');
    table_stats_form.classList.remove("table-borderless");
    const table_stats_body = table_stats_form.querySelector('tbody');

    while (table_stats_body.firstChild) {
        table_stats_body.removeChild(table_stats_body.firstChild);
    };

    const tr_element = document.createElement('tr');
    const td_element_reps = document.createElement('td');
    td_element_reps.setAttribute("class", "reps");
    const td_element_weight = document.createElement('td');
    td_element_weight.setAttribute("class", "weight");
    const td_element_save = document.createElement('td');
    td_element_save.setAttribute("class", "save");


    for (var key in dataReply["updated"]) {
        let td_reps = td_element_reps.cloneNode('true');
        td_reps.textContent = dataReply["updated"][key]["reps"];
        let td_weight = td_element_weight.cloneNode('true');
        td_weight.textContent = dataReply["updated"][key]["weight"];
        let td_save = td_element_save.cloneNode('true');
        let tr = tr_element.cloneNode('true');
        tr.appendChild(td_reps);
        tr.appendChild(td_weight);
        tr.appendChild(td_save);
        tr.setAttribute("id", `${key}`);
        table_stats_body.appendChild(tr);
    };
    
    mod_exercise.querySelector('#modify-stats-icon').innerText = "table_view";
    var form_old = table_stats_form.parentElement;
    form_old.parentElement.appendChild(table_stats_form);
    var form_add_set = mod_exercise.querySelector('form#add-set');
    form_old.parentElement.removeChild(form_add_set);
    form_old.parentElement.removeChild(form_old);

};






function updateWorkoutSet(exercise_id) {
    
    var mod_exercise = document.querySelector(`#workout-exercise-${exercise_id}`);
    var table_stats_form = mod_exercise.querySelector('#stats-form');
    table_stats_form.classList.add("table-borderless");

    var form_update = document.createElement('form');
    form_update.setAttribute("id", "form-update");
    
    table_stats_form.parentElement.appendChild(form_update);
    form_update.appendChild(table_stats_form);

    mod_exercise.querySelector('#modify-stats-icon').innerText = "";

    let input_reps = document.createElement('input');
    input_reps.className = 'form-control';
    input_reps.setAttribute("type", "number");
    input_reps.setAttribute("min", "0");
    input_reps.setAttribute("max", "100");
    input_reps.setAttribute("step", "1");
    input_reps.style.textAlign = "center";

    let input_weight = document.createElement('input');
    input_weight.className = 'form-control';
    input_weight.setAttribute("type", "number");
    input_weight.setAttribute("min", "0");
    input_weight.setAttribute("max", "300");
    input_weight.setAttribute("step", "0.01");
    input_weight.style.textAlign = "center";

    td_reps = table_stats_form.querySelectorAll('td.reps');
    td_reps.forEach(function (td_r) {
        let input_field = input_reps.cloneNode(true);
        input_field.value = td_r.innerText;
        td_r.innerText = "";
        td_r.appendChild(input_field);
    });

    td_weigth = table_stats_form.querySelectorAll('td.weight');
    td_weigth.forEach(function (td_w) {
        let input_field = input_weight.cloneNode(true);
        input_field.value = td_w.innerText;
        td_w.innerText = "";
        td_w.appendChild(input_field);
    });


    form_add = form_update.cloneNode('true');
    form_add.setAttribute("id", "add-set");
    form_update.parentNode.appendChild(form_add);

    form_add.querySelector('table').setAttribute("id", "add-form-table")
    form_add_tbody = form_add.querySelector('tbody');

    while (form_add_tbody.firstChild) {
            form_add_tbody.removeChild(form_add_tbody.firstChild);
    };

    var tr_add = document.createElement('tr');
    var td_add = document.createElement('td');

    td_add.innerText = 'Add Set:';
    tr_add.appendChild(td_add);
    form_add_tbody.appendChild(tr_add);

    let input_add_weight = input_weight.cloneNode(true);
    let input_add_reps = input_reps.cloneNode(true);
    let tr_add_stat = document.createElement('tr');
    let td_add_reps = document.createElement('td');
    td_add_reps.className = 'add-reps';
    let td_add_weight = document.createElement('td');
    td_add_weight.className = 'add-weight';

    td_add_reps.appendChild(input_add_reps);
    td_add_weight.appendChild(input_add_weight);

    tr_add_stat.appendChild(td_add_reps);
    tr_add_stat.appendChild(td_add_weight);
    
    var td_add_set = document.createElement('td');
    td_add_set.className = 'add-set';

    button_add_set = document.createElement('button');
    button_add_set.innerText = 'Add';
    button_add_set.setAttribute("type", "submit");
    button_add_set.setAttribute("name", "submit-add");
    button_add_set.classList.add('btn');
    button_add_set.classList.add('btn-warning');
    button_add_set.setAttribute.id = 'button-add-set'

    td_add_set.appendChild(button_add_set);
    tr_add_stat.appendChild(td_add_set);
    form_add_tbody.appendChild(tr_add_stat);

    form_add.addEventListener('submit', async function(event) {

        event.preventDefault();

        let new_set = {};
        let new_set_reps = mod_exercise.querySelector('td.add-reps').firstChild.value;
        let new_set_weight = mod_exercise.querySelector('td.add-weight').firstChild.value;
        
        if (new_set_reps === "") {
            new_set["reps"] = 0;    
        } else {
            new_set["reps"] = new_set_reps;
        };
        
        if (new_set_weight === "") {
            new_set["weight"] = 0;    
        } else {
            new_set["weight"] = new_set_weight;
        };
        
        if (new_set["reps"] != 0 || new_set["weight"]) {
            let dataReply = await fetchAddSet(exercise_id, new_set);
            renderUpdatedWorkoutSets(exercise_id, dataReply);
        };

    });



    td_save = table_stats_form.querySelector('td.save')
    td_save.style.verticalAlign = "center";

    tr = table_stats_form.querySelector('tr');
    button = document.createElement('button');
    span = document.createElement('span');
    span.setAttribute("class", "material-symbols-rounded");
    span.setAttribute("id", "update-icon");
    span.innerText = "save";
    button.appendChild(span);
    button.setAttribute("type", "submit");
    button.setAttribute("name", "submit");
    button.style.backgroundColor = 'rgb(0,0,0,0)';
    button.style.border = '0px';

    td_save.appendChild(button);
    console.log(document.querySelector('#form-update').querySelector('button'));

    document.querySelector('#form-update').addEventListener('submit', async function(event) {

        event.preventDefault();
        
        
        updates = {};

        tr_all = form_update.querySelectorAll('tr');
        tr_all.forEach(function (tr_a) {
            let reps = tr_a.querySelector('td.reps').querySelector('input').value;
            let weight = tr_a.querySelector('td.weight').querySelector('input').value;
            let set = {};
            set["reps"] = reps;
            set["weight"] = weight;
            updates[tr_a.id] = set;
        });    


        let dataReply = await fetchUpdateWorkoutSet(exercise_id, updates);
        renderUpdatedWorkoutSets(exercise_id, dataReply);
        
    });
};




document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll('#delete-icon').forEach(element => {

        element.onclick = function () {
            deletWorkoutExercise(this.dataset.exercise);
        };
    });


    document.querySelectorAll('#arrow-up-icon').forEach(element => {

        element.onclick = function () {
            moveUpWorkoutExercise(this.dataset.exercise);
        };
    });


    document.querySelectorAll('#arrow-down-icon').forEach(element => {

        element.onclick = function () {
            moveDownWorkoutExercise(this.dataset.exercise);
        };
    });


    document.querySelectorAll('#modify-stats-icon').forEach(element => {

        element.onclick = function () {
            updateWorkoutSet(this.dataset.exercise);
        };
    });


});

