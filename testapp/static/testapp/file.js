$(document).on('submit', '#post-form',function(e){
    e.preventDefault();
    var form = $(this).closest("form");
    $.ajax({
        type:'POST',
        url:form.attr("action") ,
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            name:$('#name').val(),
            //chapter:$('#chapter option:selected').text(),
            action: 'post'
        },
        
        success:function(json){
            document.getElementById("post-form").reset();
            //document.addEventListener('DOMContentLoaded', () => {
            //li.innerHTML = json.title + `:` + json.description;
            //document.querySelector('#messages').append(li);
            //});
            let k = 3;
            const li = document.createElement('li');
            //li.innerHTML = ;
            $(".messages").append(`<li><a href="/chapter/${json.id}"> ${json.name}</a></li>`)//
        }
    });
});