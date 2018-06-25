$('.add').on('click', function() {
  $(this).addClass('disabled');
})



$('.add_stop').on('submit', function(ev) {
  ev.preventDefault();
  $.ajax({
    method: 'POST',
    url: {{ url_for('add_stop')|tojson }},
    data: $(this).serialize()
  })
};);