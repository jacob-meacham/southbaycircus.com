// Media Library
$(function() {
    $('.btn-add-media').click(function(e) {
      getMediaLibrary($('.thumbnails'));
    });
    $('.upload-files').hide();
  });

$(function() {
  $('.btn-upload-files').click(function(e) {
    $('.media-library').hide();
    $('.upload-files').show();
  });
});

$(function() {
  var button = $('.btn-show-library');
  button.button('toggle');
  button.click(function(e) {
    $('.media-library').show();
    $('.upload-files').hide();
  });
});

$(function() {
  $('.btn-insert-media').click(function(e) {
    insertMedia();
  });
});

function selectMedia(media) {
  var img = $('<img></img>').attr('src', media.attr('src'));
  var parent = $('.select-media-pane');
  parent.empty();
  parent.append(img);
}

function getMediaLibrary(parentDiv) {
  $.get('/admin/media/library').done(function(json) {
    var mediaList = json['media'];
    $.each(mediaList, function(key, value) {
      var img = $('<img></img>').attr('src', '/static/' + value);
      var link = $('<a></a>')
        .addClass('thumbnail')
        .click(function(e) { selectMedia($(this).children('img')); })
        .append(img);
      var elem = $('<li></li>')
        .addClass('span3')
        .append(link);
      parentDiv.append(elem);
    });
  });
}

function insertMedia() {
  var val = $('#page').val(),
      strPos = $('#page')[0].selectionStart;
      front  = val.substring(0,strPos),
      back   = val.substring(strPos,val.length);
  var elem = $('<img></img>')
      .addClass('blog-image')
      .attr('src', $('.select-media-pane').children('img').attr('src'))
      .attr('style', 'display: block; margin-left: auto; margin-right: auto;');
  console.log(elem);
  $('#page').val(front + $('<div></div>').append(elem).html() + back);
}