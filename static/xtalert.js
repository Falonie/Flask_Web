var xtalert = {
    'alertError': function (msg) {
        swal('提示', msg, 'error');
    },
    'alertInfo': function (msg) {
        swal('提示', msg, 'warning');
    },
    'alertInfoWithTitle': function (title, msg) {
        swal(title, msg);
    },
    'alertSuccess': function (msg, confirmCallback) {
        args = {
            'title': '提示',
            'text': msg,
            'type': 'success'
        };
        swal(args, confirmCallback);
    },
    'alertSuccessWithTitle': function (title, msg) {
        swal(title, msg, 'success');
    },
    'alertConfirm': function (params) {
        swal({
            'title': params['title'] ? params['title'] : '提示',
            'showCancelButton': true,
            'showConfirmButton': true,
            'type': params['type'] ? params['type'] : '',
            'confirmButtonText': params['confirmText'] ? params['confirmText'] : '',
            'cancelButtonText': params['cancelText'] ? params['cancelText'] : '',
            'text': params['msg'] ? params['msg'] : ''
        }, function (isConfim) {
            if (isConfim) {
                if (params['confirmCallback']) {
                    params['confrmCallback']();
                }
            } else {
                if (params['cancelCallback']) {
                    params['cancelCallback']();
                }
            }
        });
    }
};