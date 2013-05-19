var mediaPanel = null;
function MediaPanel() {
  $('.btn-upload-files').click(function(e) {
    mediaPanel.showUpload();
  });

  var button = $('.btn-show-library');
  button.button('toggle');
  button.click(function(e) {
    mediaPanel.showLibrary();
  });

  $('.btn-insert-media').click(function(e) {
    insertMedia();
  });

  this.reset();
}

MediaPanel.prototype.reset = function() {
  $('.btn-insert-media').addClass('disabled');

  this.showLibrary();
  this.resetSelection();
};

MediaPanel.prototype.resetSelection = function() {
  if (this.selection) {
    this.selection.parent().removeClass('thumbnail-selected');
  }

  this.selection = null;
  var parent = $('.select-media-pane');
  parent.empty();

  $('.btn-insert-media').addClass('disabled');
};

MediaPanel.prototype.showLibrary = function() {
  $('.media-library').show();
  $('.upload-files').hide();
};

MediaPanel.prototype.showUpload = function() {
  $('.media-library').hide();
  $('.upload-files').show();
};

MediaPanel.prototype.selectMedia = function(selection) {
  if (this.selection) {
    this.selection.parent().removeClass('thumbnail-selected');
  }

  if (selection.is(this.selection)) {
    // Alread selected, so unselect.
    this.resetSelection();
  } else {
    this.selection = selection;
    this.selection.parent().addClass('thumbnail-selected');
    var img = $('<img></img>').attr('src', selection.attr('src'));
    var parent = $('.select-media-pane');
    parent.empty();
    parent.append(img);

    $('.btn-insert-media').removeClass('disabled');
  }
};

// Media Library
$(function() {
    mediaPanel = new MediaPanel();
    $('.btn-add-media').click(function(e) {
      getMediaLibrary($('.thumbnails'));
    });
  });

function getMediaLibrary(parentDiv) {
  mediaPanel.reset();
  $.get('/admin/media/library').done(function(json) {
    var mediaList = json['media'];
    $.each(mediaList, function(key, value) {
      var img = $('<img></img>').attr('src', '/static/' + value);
      var link = $('<a></a>')
        .addClass('thumbnail')
        .click(function(e) { mediaPanel.selectMedia($(this).children('img')); })
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