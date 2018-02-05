if (typeof NA == "undefined") window.NA = {}

NA.NAEvent = {
    doc : window.document,
    addHandler: function (element, type, handler) {
        if (element.addEventListener) {
            element.addEventListener(type, handler, false);
        } else if (element.attachEvent) {
            element.attachEvent("on" + type, handler);
        } else {
            element["on" + type] = handler;
        }
    },

    getButton: function (event) {
        if (this.doc.implementation.hasFeature("MouseEvents", "2.0")) {
            return event.button;
        } else {
            switch (event.button) {
                case 0:
                case 1:
                case 3:
                case 5:
                case 7:
                    return 0;
                case 2:
                case 6:
                    return 2;
                case 4: return 1;
            }
        }
    },

    getCharCode: function (event) {
        if (typeof event.charCode == "number") {
            return event.charCode;
        } else {
            return event.keyCode;
        }
    },

    getClipboardText: function (event) {
        var clipboardData = (event.clipboardData || window.clipboardData);
        return clipboardData.getData("text");
    },

    getEvent: function (event) {
        return event ? event : window.event;
    },

    getRelatedTarget: function (event) {
        if (event.relatedTarget) {
            return event.relatedTarget;
        } else if (event.toElement) {
            return event.toElement;
        } else if (event.fromElement) {
            return event.fromElement;
        } else {
            return null;
        }

    },

    getTarget: function (event) {
        return event.target || event.srcElement;
    },

    getWheelDelta: function (event) {
        if (event.wheelDelta) {
            return (client.engine.opera && client.engine.opera < 9.5 ? -event.wheelDelta : event.wheelDelta);
        } else {
            return -event.detail * 40;
        }
    },

    preventDefault: function (event) {
        if (event.preventDefault) {
            event.preventDefault();
        } else {
            event.returnValue = false;
        }
    },

    removeHandler: function (element, type, handler) {
        if (element.removeEventListener) {
            element.removeEventListener(type, handler, false);
        } else if (element.detachEvent) {
            element.detachEvent("on" + type, handler);
        } else {
            element["on" + type] = null;
        }
    },

    setClipboardText: function (event, value) {
        if (event.clipboardData) {
            event.clipboardData.setData("text/plain", value);
        } else if (window.clipboardData) {
            window.clipboardData.setData("text", value);
        }
    },

    stopPropagation: function (event) {
        if (event.stopPropagation) {
            event.stopPropagation();
        } else {
            event.cancelBubble = true;
        }
    }
};
//=====================COOKIE Utility==========================
NA.CookieUtil = {
    doc : window.document,
    get: function (name) {
        var cookieName = encodeURIComponent(name) + "=",
            cookieStart = this.doc.cookie.indexOf(cookieName),
            cookieValue = null,
            cookieEnd;

        if (cookieStart > -1) {
            cookieEnd = this.doc.cookie.indexOf(";", cookieStart);
            if (cookieEnd == -1) {
                cookieEnd = this.doc.cookie.length;                
            }
            cookieValue = decodeURIComponent(this.doc.cookie.substring(cookieStart + cookieName.length, cookieEnd));
        }
        return cookieValue;
    },

    set: function (name, value, expires, path, domain, secure) {
        var cookieText = encodeURIComponent(name) + "=" + encodeURIComponent(value);

        if (expires instanceof Date) {
            cookieText += "; expires=" + expires.toGMTString();
        }

        if (path) {
            cookieText += "; path=" + path;
        }

        if (domain) {
            cookieText += "; domain=" + domain;
        }

        if (secure) {
            cookieText += "; secure";
        }

        this.doc.cookie = cookieText;
    },

    unset: function (name, path, domain, secure) {
        this.set(name, "", new Date(0), path, domain, secure);
    }
};
//====================Client Utility===========================================
NA.client = function () {

    //rendering engines
    var engine = {
        ie: 0,
        gecko: 0,
        webkit: 0,
        khtml: 0,
        opera: 0,

        //complete version
        ver: null
    };

    //browsers
    var browser = {

        //browsers
        ie: 0,
        firefox: 0,
        safari: 0,
        konq: 0,
        opera: 0,
        chrome: 0,

        //specific version
        ver: null
    };


    //platform/device/OS
    var system = {
        win: false,
        mac: false,
        x11: false,

        //mobile devices
        iphone: false,
        ipod: false,
        ipad: false,
        ios: false,
        android: false,
        nokiaN: false,
        winMobile: false,

        //game systems
        wii: false,
        ps: false
    };

    //detect rendering engines/browsers
    var ua = "Mozilla/4.0 (compatible; MSIE 7.0; Windows Phone OS 7.0; Trident/3.1; IEMobile/7.0) Asus;Galaxy6";//navigator.userAgent;    
    if (window.opera) {
        engine.ver = browser.ver = window.opera.version();
        engine.opera = browser.opera = parseFloat(engine.ver);
    } else if (/AppleWebKit\/(\S+)/.test(ua)) {
        engine.ver = RegExp["$1"];
        engine.webkit = parseFloat(engine.ver);

        //figure out if it's Chrome or Safari
        if (/Chrome\/(\S+)/.test(ua)) {
            browser.ver = RegExp["$1"];
            browser.chrome = parseFloat(browser.ver);
        } else if (/Version\/(\S+)/.test(ua)) {
            browser.ver = RegExp["$1"];
            browser.safari = parseFloat(browser.ver);
        } else {
            //approximate version
            var safariVersion = 1;
            if (engine.webkit < 100) {
                safariVersion = 1;
            } else if (engine.webkit < 312) {
                safariVersion = 1.2;
            } else if (engine.webkit < 412) {
                safariVersion = 1.3;
            } else {
                safariVersion = 2;
            }

            browser.safari = browser.ver = safariVersion;
        }
    } else if (/KHTML\/(\S+)/.test(ua) || /Konqueror\/([^;]+)/.test(ua)) {
        engine.ver = browser.ver = RegExp["$1"];
        engine.khtml = browser.konq = parseFloat(engine.ver);
    } else if (/rv:([^\)]+)\) Gecko\/\d{8}/.test(ua)) {
        engine.ver = RegExp["$1"];
        engine.gecko = parseFloat(engine.ver);

        //determine if it's Firefox
        if (/Firefox\/(\S+)/.test(ua)) {
            browser.ver = RegExp["$1"];
            browser.firefox = parseFloat(browser.ver);
        }
    } else if (/MSIE ([^;]+)/.test(ua)) {
        engine.ver = browser.ver = RegExp["$1"];
        engine.ie = browser.ie = parseFloat(engine.ver);
    }

    //detect browsers
    browser.ie = engine.ie;
    browser.opera = engine.opera;


    //detect platform
    var p = navigator.platform;
    system.win = p.indexOf("Win") == 0;
    system.mac = p.indexOf("Mac") == 0;
    system.x11 = (p == "X11") || (p.indexOf("Linux") == 0);

    //detect windows operating systems
    if (system.win) {
        if (/Win(?:dows )?([^do]{2})\s?(\d+\.\d+)?/.test(ua)) {
            if (RegExp["$1"] == "NT") {
                switch (RegExp["$2"]) {
                    case "5.0":
                        system.win = "2000";
                        break;
                    case "5.1":
                        system.win = "XP";
                        break;
                    case "6.0":
                        system.win = "Vista";
                        break;
                    case "6.1":
                        system.win = "7";
                        break;
                    default:
                        system.win = "NT";
                        break;
                }
            } else if (RegExp["$1"] == "9x") {
                system.win = "ME";
            } else {
                system.win = RegExp["$1"];
            }
        }
    }

    //mobile devices
    system.iphone = ua.indexOf("iPhone") > -1;
    system.ipod = ua.indexOf("iPod") > -1;
    system.ipad = ua.indexOf("iPad") > -1;
    system.nokiaN = ua.indexOf("NokiaN") > -1;

    //windows mobile
    if (system.win == "CE") {
        system.winMobile = system.win;
    } else if (system.win == "Ph") {
        if (/Windows Phone OS (\d+.\d+)/.test(ua)) {;
            system.win = "Phone";
            system.winMobile = parseFloat(RegExp["$1"]);
        }
    }


    //determine iOS version
    if (system.mac && ua.indexOf("Mobile") > -1) {
        if (/CPU (?:iPhone )?OS (\d+_\d+)/.test(ua)) {
            system.ios = parseFloat(RegExp.$1.replace("_", "."));
        } else {
            system.ios = 2;  //can't really detect - so guess
        }
    }

    //determine Android version
    if (/Android (\d+\.\d+)/.test(ua)) {
        system.android = parseFloat(RegExp.$1);
    }

    //gaming systems
    system.wii = ua.indexOf("Wii") > -1;
    system.ps = /playstation/i.test(ua);

    //return it
    return {
        engine: engine,
        browser: browser,
        system: system
    };

}();

NA.common = {
    doc: window.document,
    //============check validity Entry Form=======================
    //InitFormValidation : function(formID,eventObject){
    //    var controls = this.doc.querySelectorAll(formID + ' :input:visible[required,patern,min,max,maxlength,type="text"]')
    //    Array.prototype.forEach.call(control, function (ctrl) {
    //        NA.NAEvent.addHandler(ctrl, 'input', function (event) {
    //            if (!this.validity.valid) {
    //                this.setCustomValidity('Please enter a valid data');                   
    //            }
    //            else {
    //                this.setCustomValidity('');
    //            }
    //        });
    //    });
    //},

    //===========cross browser get Element ByID =====================
    getElementID: function (id) {
        if (this.doc.getElementById) {
            return this.doc.getElementById(id);
        } else if (this.doc.all) {
            return this.doc.all[id];
        } else {
            throw new Error("No way to retrieve element!");
        }
    },
    //============cross browser getquerystring arguments==============
    getQueryStringArgs: function () {
        //get query string without the initial ?
        var qs = (location.search.length > 0 ? location.search.substring(1) : ""),
        //object to hold data
        args = {},
        //get individual items
        items = qs.length ? qs.split("&") : [],
        item = null,
        name = null,
        value = null,
        //used in for loop
        i = 0,
        len = items.length;
        //assign each item onto the args object
        for (i = 0; i < len; i++) {
            item = items[i].split("=");
            name = decodeURIComponent(item[0]);
            value = decodeURIComponent(item[1]);
            if (name.length) {
                args[name] = value;
            }
        }
        return args;
    },
    //==============Load Dinamic Script============================
    loadScript: function (url, Elem, id) {
        var script = this.doc.createElement("script");
        script.type = "text/javascript";
        script.src = url;
        script.setAttribute('id', id)
        if (id) {
            if (this.doc.querySelector(id) != 'undefined') {
                if (typeof (Elem) == 'undefined') {
                    this.doc.body.appendChild(script)
                }
                else {
                    elem.appendChild(script)
                }
            }
        }
        else {
            if (typeof (Elem) == 'undefined') {
                this.doc.body.appendChild(script)
            }
            else {
                elem.appendChild(script)
            }
        }
    },
    //=============Load Dynamic Style=======================
    loadStyles: function (url, id) {
        var link = this.doc.createElement("link");
        link.rel = "stylesheet";
        link.type = "text/css";
        link.href = url;
        if (id) {
            link.setAttribute('id', id)
            if (this.doc.querySelector(id) != 'undefined') {
                var head = this.doc.getElementsByTagName("header")[0];
                head.appendChild(link);
            }
        }
        else {
            var head = this.doc.getElementsByTagName("header")[0];
            head.appendChild(link);
        }
    },
    //==================Retrieving Selected Text======================
    getSelectedText: function (textbox, startIndex, stopIndex) {
        if (textbox.setSelectionRange) {
            textbox.setSelectionRange(startIndex, stopIndex);
        } else if (textbox.createTextRange) {
            var range = textbox.createTextRange();
            range.collapse(true);
            range.moveStart("character", startIndex);
            range.moveEnd("character", stopIndex - startIndex);
            range.select();
        }
        textbox.focus();
    },
    //===============ENCODE URL=================================
    addURLParam: function (url, name, value) {
        url += (url.indexOf("?") == -1 ? "?" : "&");
        url += encodeURIComponent(name) + "=" + encodeURIComponent(value);
        return url;
    },
    //================== CONVERT Object to Array ====================
    objectToArray: function (obj) {
        var _arr = [];

        for (var key in obj) {
            _arr.push([key, obj[key]]);
        }
        return _arr;
    },

    //===============Partial Text Selection=====================
    //textbox.value = “Hello world!"
    ////select all text
    //textbox.setSelectionRange(0, textbox.value.length); //"Hello world!"
    ////select first three characters
    //textbox.setSelectionRange(0, 3); //"Hel"
    ////select characters 4 through 6
    //textbox.setSelectionRange(4, 7); //"o w"

    //=======================FORM SERIALIZATION==========================
    serializeForm: function (form) {
        var parts = [],
        field = null,
        i,
        len,
        j,
        optLen,
        option,
        optValue;
        for (i = 0, len = form.elements.length; i < len; i++) {
            field = form.elements[i];
            switch (field.type) {
                case "select-one":
                case "select-multiple":
                    if (field.name.length) {
                        for (j = 0, optLen = field.options.length; j < optLen; j++) {
                            option = field.options[j];
                            if (option.selected) {
                                optValue = "";
                                if (option.hasAttribute) {
                                    optValue = (option.hasAttribute("value") ?
                                    option.value : option.text);
                                } else {
                                    optValue = (option.attributes["value"].specified ?
                                    option.value : option.text);
                                }
                                parts.push(encodeURIComponent(field.name) + "=" +
                                encodeURIComponent(optValue));
                            }
                        }
                    }
                    break;
                case undefined: //fieldset
                case "file": //file input
                case "submit": //submit button
                case "reset": //reset button
                case "button": //custom button
                    break;
                case "radio": //radio button
                case "checkbox": //checkbox
                    if (!field.checked) {
                        break;
                    }
                    /* falls through */
                default:
                    //don’t include form fields without names
                    if (field.name.length) {
                        parts.push(encodeURIComponent(field.name) + "=" +
                        encodeURIComponent(field.value));
                    }
            }
        }
        return parts.join("&");
    },
    //sebelum di compare objForm mesti di trim spacenya
    detectInputChanges: function (JsonObjInitialize, JsonObjSerializeForm) {
        var a = JSON.stringify(JsonObjInitialize), b = JSON.stringify(JsonObjSerializeForm);
        return (a.split('').sort().join('') !== b.split('').sort().join(''));
    },
    //function untuk mendisable kan element form
    //parameter form = document.form[0]/form_id
    //parameter typeofElements = type element apa saja yang akan di disabledkan
    disableForm: function (form,typeofElements) {
        var length = form.elements.length,
            i;
        for (i = 0; i < length; i++) {
            var elementType = form.elements[i].type;
            if (typeofElements) {
                if (typeofElements.indexOf(elementType) > -1) {
                    //form.elements[i].setAttribute('disabled', 'true')
                    form.elements[i].disabled = true;
                }
            }
            else {
                if (elementType === 'text' || elementType === 'textarea' || elementType === 'select' || elementType === 'checkbox') {
                    form.elements[i].disabled = true;
                }
            }            
        }
    },
    SearchData: function () {
        var elSearch = elSearch || window.document.querySelector('li.dropdown>a#bySearch');
        //valueKey   = NA.common.doc.querySelector('li.dropdown>a#bySearch').textContent.trim();
       
        var valueKey = '';//valueKey === 'By'?'':valueKey;
        var columnKey = '';//elSearch.dataset.column ? elSearch.dataset.column : 'goodsname';
        var dataType = '';//;elSearch.dataset.column ? elSearch.dataset.tipe : 'Varchar';
        var criteria = 'like';
        return {
            //==========setDefault value=================================
            setDefaultSearchData: function (defaultColumn, defaultDataType, defaultCriteria) {
                this.columnKey = defaultColumn; this.dataType = defaultDataType; this.criteria = defaultCriteria;
                this.valueKey = '';
            },
            //==========getter===============
            getValueKey: function () { return this.valueKey; },
            getColumnKey: function () { return this.columnKey; },
            getDataType: function () { return this.dataType; },
            getCriteria: function () { return this.criteria; },
            //==========setter=================
            setValue: function (nValue) { this.valueKey = nValue; },
            setColumnName: function (ncolKey) { this.columnKey = ncolKey; },
            setDataType: function (nDataType) { this.dataType = nDataType; },
            setCriteria: function (nCriteria) { this.criteria = nCriteria; },          
        }
    }(),       
};
NA.common.dialog = {
    doc: window.document,
    getPageDimensions: function () {
        var body = this.doc.getElementsByTagName("body")[0];
        var bodyOffsetWidth = 0;
        var bodyOffsetHeight = 0;
        var bodyScrollWidth = 0;
        var bodyScrollHeight = 0;
        var pageDimensions = [0, 0];

        if (typeof this.doc.documentElement != "undefined" &&
            typeof this.doc.documentElement.scrollWidth != "undefined") {
            pageDimensions[0] = this.doc.documentElement.scrollWidth;
            pageDimensions[1] = this.doc.documentElement.scrollHeight;
        }
        bodyOffsetWidth = body.offsetWidth;
        bodyOffsetHeight = body.offsetHeight;
        bodyScrollWidth = body.scrollWidth;
        bodyScrollHeight = body.scrollHeight;

        if (bodyOffsetWidth > pageDimensions[0]) {
            pageDimensions[0] = bodyOffsetWidth;
        }

        if (bodyOffsetHeight > pageDimensions[1]) {
            pageDimensions[1] = bodyOffsetHeight;
        }

        if (bodyScrollWidth > pageDimensions[0]) {
            pageDimensions[0] = bodyScrollWidth;
        }

        if (bodyScrollHeight > pageDimensions[1]) {
            pageDimensions[1] = bodyScrollHeight;
        }
        return pageDimensions;
    },
    getViewportSize: function () {
        var size = [0, 0];
        if (typeof window.innerWidth != 'undefined') {
            size = [
                window.innerWidth,
                window.innerHeight
            ];
        }
        else if (typeof this.doc.documentElement != 'undefined'
            && typeof this.doc.documentElement.clientWidth != 'undefined'
            && this.doc.documentElement.clientWidth != 0) {
            size = [
                this.doc.documentElement.clientWidth,
                this.doc.documentElement.clientHeight
            ];
        }
        else {
            size = [
                this.doc.getElementsByTagName('body')[0].clientWidth,
                this.doc.getElementsByTagName('body')[0].clientHeight
            ];
        }
        return size;
    },
    getScrollingPosition: function () {
        var position = [0, 0];

        if (typeof window.pageYOffset != 'undefined') {
            position = [
                window.pageXOffset,
                window.pageYOffset
            ];
        }
        else if (typeof this.doc.documentElement.scrollTop != 'undefined'
            && this.doc.documentElement.scrollTop > 0) {
            position = [
                this.doc.documentElement.scrollLeft,
                this.doc.documentElement.scrollTop
            ];
        }
        else if (typeof this.doc.body.scrollTop != 'undefined') {
            position = [
                this.doc.body.scrollLeft,
                this.doc.body.scrollTop
            ];
        }
        return position;
    },
    createFormContainer: function(IDForControl,placeHolderForSearch,handlerForBlurSearch,HandlerForFocusSearch,HandlerForKeyDown){
       var containerForm = this.doc.createElement("div");
       containerForm.className = 'containerForm';
       containerForm.classList.add(IDForControl);
        //create Header for Searching
        var HeaderSearching = this.doc.createElement('div');
        HeaderSearching.className = 'input-group';

   //     <div class="input-group">
   //  <input type="text" class="form-control" placeholder="Search" name="search">
   //  <div class="input-group-btn">
   //    <button class="btn btn-default" type="submit"><i class="glyphicon glyphicon-search"></i></button>
   //  </div>
   //</div>

        //create TextBox Searching with placeholder
        var searchText = this.doc.createElement('input');
        searchText.type = 'text';
        searchText.className = 'form-control';
        searchText.classList.add(IDForControl);

        searchText.id = 'txtsearch_' + IDForControl;
        searchText.setAttribute('placeholder', placeHolderForSearch);

        if (handlerForBlurSearch) {
            NA.NAEvent.addHandler(searchText, 'blur', handlerForBlurSearch);
        }
        if (HandlerForFocusSearch) {
            NA.NAEvent.addHandler(searchText, 'focus', HandlerForFocusSearch);
        }
        if (HandlerForKeyDown) {
            NA.NAEvent.addHandler(searchText, 'keydown', HandlerForKeyDown);
        }

        var inputGrButton = this.doc.createElement('div');
        inputGrButton.className = 'input-group-btn';

        var btnSearch = this.doc.createElement('button');
        btnSearch.className = 'btn';
        btnSearch.classList.add('btn-success');
        btnSearch.type = 'button';

        var Iicon = this.doc.createElement('i');
        Iicon.className = 'glyphicon';
        Iicon.classList.add('glyphicon-search');
        btnSearch.appendChild(Iicon);
        inputGrButton.appendChild(btnSearch);

        HeaderSearching.appendChild(searchText);
        HeaderSearching.appendChild(inputGrButton);

        var mainContainer = this.doc.createElement('div');
        mainContainer.className = 'maincontainerForm';
        mainContainer.classList.add(IDForControl);
        containerForm.appendChild(HeaderSearching);
        containerForm.appendChild(mainContainer);
        return containerForm;
    },
    createSearchDialog: function (event, args) {
        var body = this.doc.body;
        var pageDimensions = this.getPageDimensions();
        var viewportSize = this.getViewportSize();

        if (viewportSize[1] > pageDimensions[1]) {
            pageDimensions[1] = viewportSize[1];
        }
        var mnuContainer = this.doc.querySelector('nav.navbar.navbar-default')
        if (mnuContainer) { mnuContainer.style.zIndex = "0"; }
        var dropSheet = this.doc.createElement("div");

        dropSheet.setAttribute("id", "dropSheet");
        dropSheet.style.position = "absolute";
        dropSheet.style.left = "0";
        dropSheet.style.top = "0";

        dropSheet.style.zIndex = 1;
        dropSheet.style.width = pageDimensions[0] + "px";
        dropSheet.style.height = pageDimensions[1] + "px";
        body.appendChild(dropSheet);
        var dialog = this.doc.querySelector("div.containerDialog");
        if (!dialog) {
            dialog = this.doc.createElement("div");
            dialog.className = 'containerDialog';
            dialog.classList.add("draggable");
        }
        dialog.style.visibility = "hidden";
        dialog.style.position = "absolute";
        dialog.style.zIndex = "2";
        var scrollingPosition = this.getScrollingPosition();
        body.appendChild(dialog);
        dialog.style.left = scrollingPosition[0] + parseInt(viewportSize[0] / 3) - parseInt(dialog.offsetWidth / 2) + "px";
        dialog.style.top = scrollingPosition[1] + parseInt(viewportSize[1] / 2.5) - parseInt(dialog.offsetHeight) + "px";

        dialog.style.visibility = 'visible';

        //trigger showDialogEntry
        window.showDialogCustomSearch(event);
        //===============Enabled kan Dragdrop=================================
        NA.common.dialog.DragDrop.enable();

    },
    createDialog: function (event, args) {
        var body = this.doc.body;
        var pageDimensions = this.getPageDimensions();
        var viewportSize = this.getViewportSize();

        if (viewportSize[1] > pageDimensions[1]) {
            pageDimensions[1] = viewportSize[1];
        }
        var mnuContainer = this.doc.querySelector('nav.navbar.navbar-default')
        if (mnuContainer) { mnuContainer.style.zIndex = "0"; }
        var dropSheet = this.doc.createElement("div");

        dropSheet.setAttribute("id", "dropSheet");
        dropSheet.style.position = "absolute";
        dropSheet.style.left = "0";
        dropSheet.style.top = "0";

        dropSheet.style.zIndex = 1;
        dropSheet.style.width = pageDimensions[0] + "px";
        dropSheet.style.height = pageDimensions[1] + "px";
        body.appendChild(dropSheet);

        try {
            var dialog = this.doc.querySelector("div.containerDialog");
            if (!dialog) {
                dialog = this.doc.createElement("div");
                dialog.className = 'containerDialog';
            }
            dialog.classList.add("draggable");
            dialog.style.visibility = "hidden";
            dialog.style.position = "absolute";
            dialog.style.zIndex = "2";
            //=============create Header Dialog======================

            var headerDialog = this.doc.createElement("div");
            headerDialog.className = "ui-dialog-titlebar"
            headerDialog.classList.add("ui-corner-all");
            headerDialog.classList.add("ui-widget-header");
            headerDialog.classList.add("ui-helper-clearfix");
            headerDialog.classList.add("ui-draggable-handle");

            //create Span element
            var spanDialogTitle = this.doc.createElement('span');
            spanDialogTitle.setAttribute('id', 'ui-id-18');

            spanDialogTitle.className = "ui-dialog-title";

            //get title value from parameter
            var dialogTitle = args['dialogTitle'];
            spanDialogTitle.textContent = dialogTitle || "Nufarm Entry Data";


            //create button element
            var dialogCloseButton = this.doc.createElement("button");
            dialogCloseButton.className = "ui-button";
            dialogCloseButton.classList.add("ui-corner-all");
            dialogCloseButton.classList.add("ui-widget");
            dialogCloseButton.classList.add("ui-button-icon-only");
            dialogCloseButton.classList.add("ui-dialog-titlebar-close");
            dialogCloseButton.style.cssFloat = "right";
            dialogCloseButton.style.marginTop = "3px";
            dialogCloseButton.style.paddingLeft = ".5em";
            dialogCloseButton.style.paddingRight = ".5em"
            //create element spanDialogbutton close
            var spandialogbuttonclose = this.doc.createElement("span");
            spandialogbuttonclose.className = "ui-button-icon";
            spandialogbuttonclose.classList.add("ui-icon");
            spandialogbuttonclose.classList.add("ui-icon-closethick");
           

            var spanuibuttonIconSpace = this.doc.createElement("span");
            spanuibuttonIconSpace.className = "ui-button-icon-space";
            dialogCloseButton.appendChild(spanuibuttonIconSpace);
            dialogCloseButton.appendChild(spandialogbuttonclose);

            headerDialog.appendChild(spanDialogTitle);
            headerDialog.appendChild(dialogCloseButton);//1

            //===============create maincontendialog===============

            var mainContentDialog = this.doc.createElement("div");
            mainContentDialog.className = "maindialogContent";//2
            //isi content di loag pakai ajax Jquery(diluar object ini) setelah dialog di create


            //=============create bottom dialog=====================
            var bottomDialog = this.doc.createElement("div");
            bottomDialog.className = "bottomDialogContent";

            var dialogButtonSet1 = this.doc.createElement("div");
            dialogButtonSet1.className = "dialogButtonEntry";

            //==========create tombol OK Cancel Print dan Export==================
            //create dulu container untuk button OK Cancelnya
            dialogButtonSet1.classList.add('dialogButtonOKCancel');
            //Create tombol OK Cancel
            var btnOK = this.doc.createElement("a");
            btnOK.className = "button";
            btnOK.nodeValue = "OK";
            btnOK.textContent = "OK";
            var isDisableOK = args["btnOK"] === 'undefined' ? true : args["btnOK"];
            btnOK.style.width = "80px";
            btnOK.disabled = isDisableOK.valueOf();

            //btnOK.disabled = true;

            var btnCancel = this.doc.createElement("a");
            btnCancel.className = "button";
            btnCancel.nodeValue = "Cancel";
            btnCancel.textContent = "Cancel";
            btnCancel.style.width = "80px";
            var isDisabledCancel = args["btnCancel"] === 'undefined' ? true : args["btnCancel"];
            btnCancel.disabled = isDisabledCancel.valueOf();

            dialogButtonSet1.appendChild(btnOK);
            dialogButtonSet1.appendChild(btnCancel);


            var dialogButtonSet2 = this.doc.createElement("div");
            dialogButtonSet2.className = "dialogButtonEntry";
            dialogButtonSet2.classList.add("dialogButtonRightOther");
            //create tombol Print dan Export
            var btnPrint = this.doc.createElement("a");
            btnPrint.className = "btn-link";
            btnPrint.nodeValue = "Print Preview";
            btnPrint.textContent = "Print Preview";
            btnPrint.style.width = "120px";
            var isDisabledPrint = args["btnPrintPreview"] === 'undefined' ? true : args["btnPrintPreview"];
            btnPrint.disabled = isDisabledPrint.valueOf();
            btnPrint.style.marginRight = "0";
            btnPrint.style.paddingRight = "0";
            var btnExport = this.doc.createElement("a");
            btnExport.className = "btn-link";
            btnExport.nodeValue = "Export";
            btnExport.textContent = "Export"
            btnExport.style.width = "100px";

            var isDisabledExport = args["btnExport"] === 'undefined' ? true : args["btnPrintPreview"];
            btnExport.style.marginRight = "0";
            btnExport.style.paddingRight = "0";

            btnExport.disabled = isDisabledExport.valueOf()
            dialogButtonSet2.appendChild(btnPrint);
            dialogButtonSet2.appendChild(btnExport);


            bottomDialog.appendChild(dialogButtonSet1);
            bottomDialog.appendChild(dialogButtonSet2);//3

            dialog.appendChild(headerDialog);
            dialog.appendChild(mainContentDialog);
            dialog.appendChild(bottomDialog);

            var scrollingPosition = this.getScrollingPosition();
            body.appendChild(dialog);
            dialog.style.left = scrollingPosition[0] + parseInt(viewportSize[0] / 2) - parseInt(dialog.offsetWidth / 2) + "px";
            dialog.style.top = scrollingPosition[1] + parseInt(viewportSize[1] / 2.5) - parseInt(dialog.offsetHeight) + "px";

            dialog.style.visibility = 'visible';

            //trigger showDialogEntry
            window.showDialogEntry(event);
            //===============Enabled kan Dragdrop=================================
            NA.common.dialog.DragDrop.enable();
        }
        catch (error) {
            this.closeDialog(dialog);
            var mnuContainer = doc.querySelector('nav.navbar.navbar-default')
            if (mnuContainer) { mnuContainer.style.zIndex = "1000"; }
            return true;
        }
        return false;
    },
    closeDialog: function (dialog) {
        var dropSheet = NA.common.getElementID("dropSheet");
        if (dropSheet) {
            dropSheet.parentNode.removeChild(dropSheet);
            //remove attribute container dialog    
            NA.common.dialog.DragDrop.disable();
            if (dialog) {
                dialog.parentNode.removeChild(dialog);
            }
        }       
        var mnuContainer = this.doc.querySelector('nav.navbar.navbar-default')
        if (mnuContainer) { mnuContainer.style.zIndex = "1000"; }

        return false;
    },
    //parameters
    //Entrycontnr = menu add edit delete ---> NA.common.dialog.doc.querySelector('ul.nav.navbar-nav')
    //titleHeader = Header dialog title
    //elementMenus = array component yang akan di pakai untuk click menu di side bar
    // SideMenuContainerClick = custom event handler yang akan mengeksekusi bila click event dalam array menu di click, default tidak usah di isi saja
    initDialog: function (Entrycontnr, titleHead, elementMenus, SideMenuContainerClick) {

        // init dialog untuk Open,  Edit,  Save,  Delete,  Export,  Print,  Help        
        (function (elem, currentObj, titleHead, elements, otherHandler) {
            var settingsEditAdd = { btnOK: true, btnCancel: true, btnPrintPreview: true, btnExport: false, dialogTitle: titleHead },
			settingsOpen = { btnOK: false, btnCancel: false, btnPrintPreview: false, btnExport: false, dialogTitle: titleHead };
            settingsOther = { btnOK: true, btnCancel: true, btnPrintPreview: true, btnExport: true, dialogTitle: titleHead };
            //menu atas
            var ClickHandlerElem = function (event) {
                NA.NAEvent.preventDefault(event);
                var target = NA.NAEvent.getTarget(event);
                switch (target.innerText) {
                    case ' Add': {
                        if (!target.getAttribute('disabled')) {
                            currentObj.createDialog(event, settingsEditAdd);
                            window.status = "Add"
                        }
                        break;
                    }
                    case ' Open': {
                        currentObj.createDialog(event, settingsOpen);
                        window.status = "Open"
                        break;
                    }
                    case ' Edit': {
                        currentObj.createDialog(event, settingsEditAdd);
                        window.status = "Edit"
                        break;
                    }
                    default: { window.status = ""; break; }
                }
            };
            if (elem) {
                NA.NAEvent.addHandler(elem, 'click', ClickHandlerElem);
            }

            //menu side
            var ClickHandlerElementMenu = function (event) {
                NA.NAEvent.preventDefault(event);
                currentObj.createDialog(event, settingsOther);
                window.status = "";
            };
            if (elements) {
                Array.prototype.forEach.call(elements, function (item) {//buat jadi foreach mesti convert dulu ke array
                    if (SideMenuContainerClick) {
                        if (!item.getAttribute('disabled')) {
                            NA.NAEvent.addHandler(item, 'click', SideMenuContainerClick);
                        }
                    }
                    else {
                        if (!item.getAttribute('disabled')) {
                            NA.NAEvent.addHandler(item, 'click', ClickHandlerElementMenu);
                        }                       
                    }
                });
            }
        })(Entrycontnr, this, titleHead, elementMenus, SideMenuContainerClick);

    },// Save,  Delete,  Export,  Print,  Help
    //=================================Enabbled DragDrop Dialog==============================================================================
    DragDrop: function () {

        var dragging = null;

        function handleEvent(event) {

            //get event and target
            event = NA.NAEvent.getEvent(event);
            var target = NA.NAEvent.getTarget(event);

            //determine the type of event
            switch (event.type) {
                case "mousedown":
                    if (target.className.indexOf("draggable") > -1) {
                        dragging = target;
                    }
                    break;

                case "mousemove":
                    if (dragging !== null) {

                        //assign location
                        dragging.style.left = event.clientX + "px";
                        dragging.style.top = event.clientY + "px";
                    }
                    break;

                case "mouseup":
                    dragging = null;
                    break;
            }
        };

        //public interface
        return {
            enable: function () {
                //var dialog = NA.common.dialog.doc.querySelector("div.containerDialog");
                NA.NAEvent.addHandler(window.document, "mousedown", handleEvent);
                NA.NAEvent.addHandler(window.document, "mousemove", handleEvent);
                NA.NAEvent.addHandler(window.document, "mouseup", handleEvent);
            },
            disable: function () {
                NA.NAEvent.removeHandler(window.document, "mousedown", handleEvent);
                NA.NAEvent.removeHandler(window.document, "mousemove", handleEvent);
                NA.NAEvent.removeHandler(window.document, "mouseup", handleEvent);
            }
        }
    }(),
};
//=========================AJAX NAJS,(belum di test) =============================================
NA.common.AJAX = {
    XHR:{},
    Xsettings: {
        data: {},
        dataType: 'application/json',//content yang di kirim ke server jika post default nya application/json
        url: '',
        MIMEType: 'text/html',//method overrides the MIME type returned by the server,default 'text/html',override responsetype
        timeOut: 2000000
    },
};
NA.common.AJAX.createXHR = function () {
    if (typeof XMLHttpRequest != "undefined") {
        this.XHR = new XMLHttpRequest();
    } else if (typeof ActiveXObject != "undefined") {
        if (typeof arguments.callee.activeXString != "string") {
            var versions = ["MSXML2.XMLHttp.6.0", "MSXML2.XMLHttp.3.0",
                            "MSXML2.XMLHttp"],
                i, len;
            for (i = 0, len = versions.length; i < len; i++) {
                try {
                    var xhr = new ActiveXObject(versions[i]);
                    arguments.callee.activeXString = versions[i];
                    return xhr;
                } catch (ex) {
                    //skip
                }
            }
        }
        this.XHR = new ActiveXObject(arguments.callee.activeXString);
    } else {
        throw new Error("No XHR object available.");
    }
    return this.XHR;
};
Object.defineProperty(NA.common.AJAX, 'settings', {
    get: function () {
        return this.Xsettings || {}
    },
    set: function (newSettings) {
        //var Xsettings = this.Xsettings || {};
        //Xsettings.data = data || {};
        //Xsettings.dataType = dataType || 'application/json';//content yang di kirim ke server jika post default nya application/json
        //Xsettings.url = url || '';
        //Xsettings.MIMEType = MType || 'text/html';//method overrides the MIME type returned by the server,default 'text/html',override responsetype
        //Xsettings.requestHeader = requestHeader || {};
        //Xsettings.timeOut = timeOut || 2000000;
        this.Xsettings = newSettings;
    }
});
NA.common.AJAX.POST = function (url, data, dataType, MIMEType, OnAJAXStart, OnBeforeSend, OnLoad, OnProgress, OnError, OnLoadEnd, customRequestHeader) {
    if (!this.XHR) { this.createXHR(); }
    var Xurl = url || this.settings.url;
    if (!Xurl || Xurl === '') {
        throw new Error("Please define URL");
    }
    var XData = data || this.settings.data, XdataType = dataType || this.settings.dataType;
    if (OnAJAXStart) { OnAJAXStart.call(this.XHR); }
    this.XHR.overrideMimeType(MIMEType || this.settings.MIMEType);
    if (onload) { this.XHR.onload = OnLoad; }
    if (OnProgress) { this.XHR.onprogress = OnProgress; }
    if (OnError) { this.XHR.onerror = OnError; }
    if (OnLoadEnd) { this.XHR.onloadend = OnLoadEnd; }
    this.XHR.open('POST', Xurl, true);
    if (typeof customRequestHeader != 'undefined' && customRequestHeader !== '' && customRequestHeader != {})
    { this.XHR.setRequestHeader(customRequestHeader.key, customRequestHeader.value); }
    this.XHR.setRequestHeader('Content-Type', XdataType);
    //==========prevent browser catching============================
    this.XHR.setRequestHeader('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0');
    this.XHR.setRequestHeader('Pragma', 'no - cache');
    this.XHR.setRequestHeader('Expires', 'Thu, 19 Nov 1981 08:52:00 GMT');
    //==============================================================
    //XHR.setRequestHeader('Accept :' + XdataType);
    if (OnBeforeSend) { OnBeforeSend.call(this.XHR); }
    if (XData) { this.XHR.send(XData); }
    return true;
};
NA.common.AJAX.GET = function (url, MIMEType, OnAJAXStart, OnBeforeSend, OnLoad, OnProgress, OnError, OnLoadEnd, customRequestHeader) {
    if (!this.XHR) { this.createXHR(); }
    var Xurl = url || this.settings.url;
    if (!Xurl || Xurl === '') {
        throw new Error("Please define URL");
    }
    var XData = data || this.settings.data, XdataType = dataType || this.settings.dataType;
    if (OnAJAXStart) { OnAJAXStart.call(this.XHR); }
    this.XHR.overrideMimeType(MIMEType || this.settings.MIMEType);
    if (onload) { this.XHR.onload = OnLoad; }
    this.XHR.open('GET', Xurl, true);
    if (OnProgress) { this.XHR.onprogress = OnProgress; }
    if (OnError) { this.XHR.onerror = OnError; }
    if (OnLoadEnd) { this.XHR.onloadend = OnLoadEnd; }
    if (typeof customRequestHeader != 'undefined' && customRequestHeader !== '' && customRequestHeader != {})
    { this.XHR.setRequestHeader(customRequestHeader.key, customRequestHeader.value); }
    this.XHR.setRequestHeader('Content-Type', XdataType);
    //==========prevent browser catching============================
    this.XHR.setRequestHeader('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0');
    this.XHR.setRequestHeader('Pragma', 'no - cache');
    this.XHR.setRequestHeader('Expires', 'Thu, 19 Nov 1981 08:52:00 GMT');
    //==============================================================
    if (OnBeforeSend) { OnBeforeSend.call(this.XHR); }
    this.XHR.send(null);
    return true;
};
NA.common.AJAX.SubmitForm = function (url, FormElement, MIMEType, OnAJAXStart, OnBeforeSend, OnLoad, OnProgress, OnError, OnLoadEnd, customRequestHeader) {
    if (!this.XHR) { this.createXHR(); }
    var Xurl = url || this.settings.url;
    if (!Xurl || Xurl === '') {
        throw new Error("Please define URL");
    }
    var XData = data || this.settings.data, XdataType = dataType || this.settings.dataType;
    if (OnAJAXStart) { OnAJAXStart.call(this.XHR); }
    this.XHR.overrideMimeType(MIMEType || this.settings.MIMEType);
    if (onload) { this.XHR.onload = OnLoad; }
    this.XHR.open('POST', Xurl, true);
    if (typeof customRequestHeader != 'undefined' && customRequestHeader !== '' && customRequestHeader != {})
    { this.XHR.setRequestHeader(customRequestHeader.key, customRequestHeader.value); }
    this.XHR.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    //==========prevent browser catching============================
    this.XHR.setRequestHeader('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0');
    this.XHR.setRequestHeader('Pragma', 'no - cache');
    this.XHR.setRequestHeader('Expires', 'Thu, 19 Nov 1981 08:52:00 GMT');
    //==============================================================
    this.XHR.send(NA.common.serializeForm(FormElement));
    return true;
};
//NA.common.AJAX = function(){
//    function createXHR(){
//        if (typeof XMLHttpRequest != "undefined"){
//            return new XMLHttpRequest();
//        } else if (typeof ActiveXObject != "undefined"){
//            if (typeof arguments.callee.activeXString != "string"){
//                var versions = ["MSXML2.XMLHttp.6.0", "MSXML2.XMLHttp.3.0",
//                                "MSXML2.XMLHttp"],
//                    i, len;            
//                for (i=0,len=versions.length; i < len; i++){
//                    try {
//                        var xhr = new ActiveXObject(versions[i]);
//                        arguments.callee.activeXString = versions[i];
//                        return xhr;
//                    } catch (ex){
//                        //skip
//                    }
//                }
//            }            
//            return new ActiveXObject(arguments.callee.activeXString);
//        } else {
//            throw new Error("No XHR object available.");
//        }
//    };
//    var XHR = null;
//    var settings = settings || {};
//    settings.data = settings.data || {};
//    settings.dataType = settings.dataType || 'application/json';//content yang di kirim ke server jika post default nya application/json
//    settings.url = settings.url || '';
//    settings.MIMEType = settings.MIMEType || 'text/html';//method overrides the MIME type returned by the server,default 'text/html',override responsetype
//    settings.requestHeader = settings.requestHeader || '';
//    settings.timeOut = settings.timeOut || 2000000;
//    function create(){
//        if (XHR == null || typeof XHR == 'undefined') {
//            XHR = createXHR();
//        }
//        return XHR;
//    };
//    function XHRSetting(){
//        return settings;
//    }
//    return XHR;
 
    //return {
    //    NAXHR: function () { return XHR; },//get XHR reference
    //    create: function () { }},
    //    XHRSettings: function(){},
    //    POST: function (url, data, dataType, MIMEType, OnAJAXStart, OnBeforeSend, OnLoad, OnProgress, OnError, OnLoadEnd, customRequestHeader) {
            
    //        var Xurl = url || settings.url ;
    //        if (!Xurl || Xurl ==='') {
    //            throw new Error("Please define URL");
    //        }
    //        var XData = data || settings.data, XdataType = dataType || settings.dataType;
    //        if (OnAJAXStart) { OnAJAXStart.call(XHR); }
    //        XHR.overrideMimeType(MIMEType || settings.MIMEType);
            
    //        if (onload) { XHR.onload = OnLoad; }
    //        if (OnProgress) { XHR.onprogress = OnProgress; }
    //        if (OnError) { XHR.onerror = OnError; }
    //        if (OnLoadEnd) { XHR.onloadend = OnLoadEnd; }          
    //        XHR.open('POST', Xurl, true);
    //        if (typeof customRequestHeader != 'undefined' && customRequestHeader !== '' && customRequestHeader != {})
    //        { XHR.setRequestHeader(customRequestHeader.key, customRequestHeader.value); }
    //        XHR.setRequestHeader('Content-Type', XdataType);
    //        //==========prevent browser catching============================
    //        XHR.setRequestHeader('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0');
    //        XHR.setRequestHeader('Pragma', 'no - cache');
    //        XHR.setRequestHeader('Expires', 'Thu, 19 Nov 1981 08:52:00 GMT');
    //        //==============================================================
    //        //XHR.setRequestHeader('Accept :' + XdataType);
    //        if (OnBeforeSend) { OnBeforeSend.call(XHR); }
    //        if (XData) { XHR.send(XData); }
    //    },
    //    GET: function (url, MIMEType, OnAJAXStart, OnBeforeSend, OnLoad, OnProgress, OnError, OnLoadEnd, customRequestHeader) {
    //        var Xurl = url || settings.url;
    //        if (!Xurl || Xurl === '') {
    //            throw new Error("Please define URL");
    //        }          
    //        if (OnAJAXStart) { OnAJAXStart.call(XHR); }
    //        XHR.overrideMimeType(MIMEType || settings.MIMEType);

    //        if (onload) { XHR.onload = OnLoad; }
    //        if (OnProgress) { XHR.onprogress = OnProgress; }
    //        if (OnError) { XHR.onerror = OnError; }
    //        if (OnLoadEnd) { XHR.onloadend = OnLoadEnd; }        
    //         XHR.open('GET', Xurl, true);
    //        if (typeof customRequestHeader != 'undefined' && customRequestHeader !== '' && customRequestHeader != {})
    //        { XHR.setRequestHeader(customRequestHeader.key, customRequestHeader.value); }
    //        XHR.setRequestHeader('Content-Type', XdataType);
    //        //==========prevent browser catching============================
    //        XHR.setRequestHeader('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0');
    //        XHR.setRequestHeader('Pragma', 'no - cache');
    //        XHR.setRequestHeader('Expires', 'Thu, 19 Nov 1981 08:52:00 GMT');
    //        //==============================================================
    //        if (OnBeforeSend) { OnBeforeSend.call(XHR); }
    //        XHR.send(null);
    //    },
    //    SubmitForm: function (url, FormElement, MIMEType, OnAJAXStart, OnBeforeSend, OnLoad, OnProgress, OnError, OnLoadEnd, customRequestHeader) {
    //        var Xurl = url || settings.url;
    //        if (!Xurl || Xurl === '') {
    //            throw new Error("Please define URL");
    //        }
    //        if (OnAJAXStart) { OnAJAXStart.call(XHR); }
    //        XHR.overrideMimeType(MIMEType || settings.MIMEType);
    //        if (onload) { XHR.onload = OnLoad; }
    //        if (OnProgress) { XHR.onprogress = OnProgress; }
    //        if (OnError) { XHR.onerror = OnError; }
    //        if (OnLoadEnd) { XHR.onloadend = OnLoadEnd; }
    //        XHR.open('POST', Xurl, true);
    //        if (typeof customRequestHeader != 'undefined' && customRequestHeader !== '' && customRequestHeader != {})
    //        { XHR.setRequestHeader(customRequestHeader.key, customRequestHeader.value); }
    //        XHR.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    //        //==========prevent browser catching============================
    //        XHR.setRequestHeader('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0');
    //        XHR.setRequestHeader('Pragma', 'no - cache');
    //        XHR.setRequestHeader('Expires', 'Thu, 19 Nov 1981 08:52:00 GMT');
    //        //==============================================================
    //        XHR.send(NA.common.serializeForm(FormElement));
    //    },
    //};
//}
//=================================================================
   
