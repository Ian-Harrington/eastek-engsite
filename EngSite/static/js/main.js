function addDeleteForms() {
    function updateFormIds() {
        var forms = $('.form');
        $('#id_form-TOTAL_FORMS').val(forms.length);
        for (i = 0; i <= forms.length; i+=1) {
            elem = $(forms.get(i)).children().children();
            elem.each(function () {$(this).attr('id', $(this).attr('id').replace(/form-(\d+)-/, 'form-'+i+'-'));});
        }
    }

    $('#add-form').on('click', function() {
        var form_index = $('.form').length;
        $('.form:last').after($('#empty-form').children().html().replace(/__prefix__/g, parseInt(form_index)).replace(/fake-form/, 'form'));
        addDeleteHandlers();
        form_index = $('.form').length;
        $('#id_form-TOTAL_FORMS').val(parseInt(form_index));
        return false;
    });

    function addDeleteHandlers () {
        $('.delete-form').on('click', function() {
            $(this).parents('.form').remove();
            updateFormIds();
            return false;
        });
    }
    
    addDeleteHandlers();
    $('#id_form-TOTAL_FORMS').val($(".form").length);
    $(".form").children().children().removeAttr('name', "");
    $(".fake-form").children().children().removeAttr('name', "");
}


function changeLang() {
    function createCookie(name,value,days) {
        var expires = "";
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days*24*60*60*1000));
            expires = "; expires=" + date.toUTCString();
        }
    document.cookie = name + "=" + value + expires + "; path=/";
    }

    $("#set-lang-en").on('click', function () {return createCookie('language', 'en', 20000)});
    $("#set-lang-zh").on('click', function () {return createCookie('language', 'zh-hans', 20000)});
}