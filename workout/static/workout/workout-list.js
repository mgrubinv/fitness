document.addEventListener('DOMContentLoaded', function () {

    let customer = window.location.pathname.split('/')[2];
    
    let select = document.getElementById('filter_customer');
    if (customer != null) {
        select.value = customer;
    } else {
        select.value = 0;
    };
    
    
    


});