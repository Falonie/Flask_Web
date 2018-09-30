$(function () {
    $('#save-banner-btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $('#banner-dialog');
        var name_input = $("input[name='name']");
        var image_url_input = $("input[name='image_url']");
        var link_url_input = $("input[name='link_url']");
        var priority_input = $("input[name='priority']");

        var name = name_input.val();
        var image_url = image_url_input.val();
        var link_url = link_url_input.val();
        var priority = priority_input.val();
        var submitType = self.attr('data-type');
        var bannerid = self.attr('data-id');

        if (!name || !image_url || !link_url || !priority) {
            zlalert.alertInfoToast('请输入完整轮播图数据');
            return;
        }

        var url = '';
        if (submitType == 'update') {
            url = '/cms/upbanner/'
        } else {
            url = '/cms/abanner/'
        }

        zlajax.post({
            'url': url,
            'data': {
                'name': name,
                'image_url': image_url,
                'link_url': link_url,
                'priority': priority,
                'banner_id': bannerid
            },
            'success': function (data) {
                dialog.modal('hide');
                if (data['code'] == 200) {
                    // 重新加载这个页面
                    window.location.reload();
                } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function () {
                zlalert.alertNetworkError();
            }
        })
    });
});

$(function () {
    $('.edit-banner-btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $('#banner-dialog');
        dialog.modal('show');

        var tr = self.parent().parent();
        var name = tr.attr("data-name");
        var imgae = tr.attr("data-image");
        var link = tr.attr("data-link");
        var priority = tr.attr("data-priority");

        var name_input = dialog.find("input[name='name']");
        var image_url_input = dialog.find("input[name='image_url']");
        var link_url_input = dialog.find("input[name='link_url']");
        var priority_input = dialog.find("input[name='priority']");
        var saveBtn = dialog.find('#save-banner-btn');

        name_input.val(name);
        image_url_input.val(imgae);
        link_url_input.val(link);
        priority_input.val(priority);
        saveBtn.attr('data-type', 'update');
        saveBtn.attr('data-id', tr.attr('data-id'));
    });
});

$(function () {
    $('.delete-banner-btn').click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var banner_id = tr.attr('data-id');
        zlalert.alertConfirm({
            'msg': '确定删除轮播图',
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/dbanner/',
                    'data': {
                        'banner_id': banner_id
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            window.location.reload();
                        } else {
                            zlert.alertInfo(data['message']);
                        }
                    }
                })
            }
        });
    });
});

$(function () {
    zlqiniu.setUp({
        'domain': 'http;//7xqenu.com1.z0.glb.clouddn.com/',
        'browse_btn': 'upload-btn',
        'uptoken_url': '/c/uptoken/',
        'success': function (up, file, info) {
            // var image_url = file.name;
            // var imageInput = document.getElementById('image-input');
            // imageInput.value = image_url;
            // var img = document.getElementById('img');
            // img.getAttribute('src', image_url);
            var imageInput = $("input[name='image_url']");
            imageInput.val(file.name);
        }
    });
});