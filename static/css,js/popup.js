/*text-to-img*/
function popupShow(){
    $(".popup").show();
    /*버튼 효과*/
    const btn = document.getElementById('style_button1')
        
    const onClick = d => {
        const { x, y, width, height} = btn.getBoundingClientRect()
        const radius = Math.sqrt(width * width + height * height)
        btn.style.setProperty('--diameter', radius * 2 + 'px')
        const { clientX, clientY } = d
        const left = (clientX - x - radius) / width * 100 + '%'
        const top = (clientY - y - radius) / height * 100 + '%'
    
        btn.style.setProperty('--left', left)
        btn.style.setProperty('--top', top)
        btn.style.setProperty('--a', '')
        setTimeout(() => {
            btn.style.setProperty('--a', 'ripple-effect 500ms linear')
        }, 5)
    }    
    btn.addEventListener('click', onClick)

    popupShutdown2();
    popupShutdown3();
    popupShutdown4();
}
function popupShutdown(){
  $(".popup").hide();
}

/*img-to-img*/
function popupShow2(){
  $(".popup2").show();    
  /*버튼 효과*/
  const btn2 = document.getElementById('style_button2');
  
  const onClick2 = d => {
      const { x, y, width, height} = btn2.getBoundingClientRect();
      const radius = Math.sqrt(width * width + height * height);
      btn2.style.setProperty('--diameter', radius * 2 + 'px');
      const { clientX, clientY } = d;
      const left = (clientX - x - radius) / width * 100 + '%';
      const top = (clientY - y - radius) / height * 100 + '%';
  
      btn2.style.setProperty('--left', left);
      btn2.style.setProperty('--top', top);
      btn2.style.setProperty('--a', '');
      setTimeout(() => {
          btn2.style.setProperty('--a', 'ripple-effect 500ms linear');
      }, 5);
  }
  btn2.addEventListener('click', onClick2);
  
  /*canvas 그림 보내기*/
  var userid=document.getElementById('user');
  var canvas = document.getElementById('cnvs');
  var imagePromptInput = document.getElementById('prompt');
  var imageNPromptInput= document.getElementById('nprompt');
  var ifilter=document.getElementById("sfilter2");
  var icfg=document.querySelector('select[id="icfg"]');
  var isteps=document.getElementById("isteps");
  var inoise=document.getElementById("noise");
  const sendBtn = document.getElementById('sendBtn');
  var oshare=document.getElementById('open2')
  var cshare=document.getElementById('close2')
  var ishare
  // 체크된 상태인지 확인하고 값 가져오기
  if (oshare.checked) {
    ishare = "1";
    }
  if (cshare.checked) {
    ishare = "0";
    }

  sendBtn.addEventListener('click', function () {
      const id=userid.value;
      const stdname="Img to Img"
      const share=ishare;
      const imagePromptText = imagePromptInput.value;
      const imageNPromptText=imageNPromptInput.value;
      const cfg=icfg.value;
      const steps=isteps.value;
      const noise=inoise.value;
      const filter=ifilter.value;

      canvas.toBlob(function (blob) {
          const formData = new FormData();
          formData.append('userid', id);
          formData.append('stdname', stdname);
          formData.append('share', share)
          formData.append('image_prompt_text', imagePromptText);
          formData.append('image_nprompt_text', imageNPromptText);
          formData.append('filter', filter);
          formData.append('cfg', cfg);
          formData.append('steps',steps);
          formData.append('noise', noise);

          const xhr = new XMLHttpRequest();
          xhr.open('POST', '/change_image', true);
          xhr.onreadystatechange = function () {
              if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                //console.log(xhr.responseText)
                var response = JSON.parse(xhr.responseText); // Parse the response
                var image_url=response.image_file;
                closeResult();
                openResult(image_url);
              }
          };
          xhr.send(formData);
      }, 'image/png');
  });

  popupShutdown();            
  popupShutdown3();
  popupShutdown4();
}
function popupShutdown2(){
  $(".popup2").hide();
}

/*InPainting*/
function popupShow3(){
  $(".popup3").show();
  /*버튼 효과*/
  const btn3 = document.getElementById('style_button3');

  const onClick3 = d => {
      const { x, y, width, height} = btn3.getBoundingClientRect();
      const radius = Math.sqrt(width * width + height * height);
      btn3.style.setProperty('--diameter', radius * 2 + 'px');
      const { clientX, clientY } = d;
      const left = (clientX - x - radius) / width * 100 + '%';
      const top = (clientY - y - radius) / height * 100 + '%';

      btn3.style.setProperty('--left', left);
      btn3.style.setProperty('--top', top);
      btn3.style.setProperty('--a', '');
      setTimeout(() => {
          btn3.style.setProperty('--a', 'ripple-effect 500ms linear');
      }, 5);
  }

  btn3.addEventListener('click', onClick3);

  /*canvas 그림 보내기*/  
  var userid=document.getElementById('user');
  var inshare=document.querySelector('share[id="inshare"]')
  var canvas = document.getElementById('cnvs3');
  var imagePromptInput = document.getElementById('inpaint_prompt');
  var imageNPromptInput=document.getElementById('inpaint_nprompt');
  var filter=document.getElementById("sfilter3");
  const sendBtn3 = document.getElementById('sendBtn3');
  var oshare=document.getElementById('open3')
  var cshare=document.getElementById('close3')
  var inshare
  // 체크된 상태인지 확인하고 값 가져오기
  if (oshare.checked) {
    inshare = "1";
    }
  if (cshare.checked) {
    inshare = "2";
    }

  
  sendBtn3.addEventListener('click', function () {
      const id=userid.value;
      const stdname="InPaint"
      const share=inshare;

      canvas.toBlob(function (blob) {
          const formData = new FormData();
          formData.append('userid', id);
          formData.append('stdname', stdname);
          formData.append('share', share)
          formData.append('image_prompt_text', imagePromptInput.value);
          formData.append('image_nprompt_text', imageNPromptInput.value);
          formData.append('filter', filter.value);
  
          const xhr = new XMLHttpRequest();
          xhr.open('POST', '/inpainting_image', true);
          xhr.onreadystatechange = function () {
              if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                //console.log(xhr.responseText)
                var response = JSON.parse(xhr.responseText); // Parse the response
                var image_url=response.image_file;
                closeResult();
                openResult(image_url);
              }
          };
          xhr.send(formData);
      }, 'image/png');
  });
  
  popupShutdown();
  popupShutdown2();
  popupShutdown4();
}
function popupShutdown3(){
  $(".popup3").hide();
}
  
/*Open Pose*/
function popupShow4(){
  $(".popup4").show();
  /*버튼 효과*/
  const btn4 = document.getElementById('style_button4');

  const onClick4 = d => {
    const { x, y, width, height} = btn4.getBoundingClientRect();
    const radius = Math.sqrt(width * width + height * height);
    btn4.style.setProperty('--diameter', radius * 2 + 'px');
    const { clientX, clientY } = d;
    const left = (clientX - x - radius) / width * 100 + '%';
    const top = (clientY - y - radius) / height * 100 + '%';

    btn4.style.setProperty('--left', left);
    btn4.style.setProperty('--top', top);
    btn4.style.setProperty('--a', '');
    setTimeout(() => {
      btn4.style.setProperty('--a', 'ripple-effect 500ms linear');
    }, 5);
  }

  btn4.addEventListener('click', onClick4);
  
  popupShutdown();
  popupShutdown3();
  popupShutdown2();
}
function popupShutdown4(){
  $(".popup4").hide();
}

