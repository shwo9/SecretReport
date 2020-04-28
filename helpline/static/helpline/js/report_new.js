// Pagenation


// function msg() {
//   document.getElementById("confirm").setAttribute('href', "http://www.naver.com");
// }


var page = 1;

function manageButton() {
  var prevEl = document.getElementById("prev");
  var nextEl = document.getElementById("next");

  if (page === 1) {
    prevEl.style.display = "none";
  } else if (page === 5) {
    nextEl.innerHTML = "확인";
  } else {
    prevEl.style.display = "block";
    nextEl.innerHTML = "다음";
  }
}

function prevPage() {
  var prevEl = document.getElementById("step_" + page);
  prevEl.style.display = "none";

  page -= 1;
  var currentEl = document.getElementById("step_" + page);
  currentEl.style.display = "flex";

  lightIndex(page);
  manageButton();
}

function nextPage() {
  let flag = false;

  switch (page) {
    case 1:
      flag = validationPageOne();
      break;
    case 2:
      flag = validationPageTwo();
      break;
    case 3:
      flag = validationPageThree();
      break;
    case 4:
      flag = validationPageFour();
      break;
    case 5:
      document.getElementById("declare_form").submit();
      break;
  }

  if (flag.length !== 0) {
    displayError(flag);
    return;
  }

  var prevEl = document.getElementById("step_" + page);
  prevEl.style.display = "none";

  page += 1;
  var currentEl = document.getElementById("step_" + page);
  currentEl.style.display = "flex";

  lightIndex(page);
  manageButton();
  hiddenError();

  if (page === 5) bindingData();
}

function lightIndex(index) {
  var process_indexs = document.querySelectorAll(".process_index");

  for (var i = 0; i < process_indexs.length; i++) {
    process_indexs[i].style.background = "#91a7ff";
  }

  process_indexs[index - 1].style.background = "#4c6ef5";
}

// Validation Functions along with pages

function validationPageOne() {
  var value_1 = "2",
    value_2 = false;
  document.querySelectorAll('input[name="agreement_1"]').forEach(e => {
    if (e.checked) value_1 = e.value;
  });
  document.querySelectorAll('input[name="agreement_2"]').forEach(e => {
    if (e.checked) value_2 = true;
  });
  if (!(value_1 == "1" && value_2)) return "신분 정보 제공에 관한 동의여부에 체크해주세요."
  return ""
}

function validationPageTwo() {
  let flag = true;
  document.querySelectorAll(".form_certification input").forEach(el => {
    if (el.id !== "detailAddress") {
      if (el.value === null || el.value === "") flag = false;
    }
  });

  if (!flag) "정보 입력 및 본인인증을 해주세요."
  return ""
}

function validationPageThree() {
  let flag = true,
    pwFlag = false,
    checkPW = false,
    radioFlag_1 = false,
    radioFlag_2 = false,
    checkboxFlag = false;

  var passwordRegex = /(?=.*\d{1,})(?=.*[~`!@#$%\^&*()-+=]{1,})(?=.*[a-zA-Z]{1,}).{8,50}$/;

  document.querySelectorAll(".form_declare input").forEach(el => {
    switch (el.type) {
      case "file":
        break;
      case "radio":
        if (el.name === "grasp" && el.checked) radioFlag_1 = true;
        if (el.name === "term" && el.checked) radioFlag_2 = true;
        break;
      case "checkbox":
        if (el.checked) checkboxFlag = true;
        break;
      case "password":
        pwFlag = passwordRegex.test(el.value);
        if (document.getElementById("password").value === document.getElementById("re_password").value) {
          checkPW = true;
        }

        break;
      default:
        if (el.value === null || el.value === "") flag = false;
    }
  });
  if (!pwFlag) return "비밀번호는 8자 이상의 영문 대소문자,숫자,특수문자를 포함해야 합니다."
  else if (!checkPW) return "입력하신 비밀번호가 일치하지 않습니다."
  else if (!(flag && radioFlag_1 && radioFlag_2 && checkboxFlag)) return "신고서를 작성하는 데 필요한 정보를 모두 입력해주세요."
  else return ""
}

function validationPageFour() {
  let flag = false;

  document.querySelectorAll('input[name="lawyer"]').forEach(el => {
    if (el.checked) flag = true;
  });

  if (!flag) return "변호사를 선택해주세요."
  return ""
}

function displayError(msg) {
  errorEl = document.querySelector(`#step_${page} .error`);


  switch (page) {
    case 5:
      document.getElementById("declare_form").submit();
      break;
    default:
      errorEl.innerHTML = msg;
      break;
  }
}

function hiddenError() {
  document.querySelectorAll(`.error`).forEach(el => {
    el.innerHTML = "";
  });
}

// Cleave Library for Input Format

var rrnCleave = new Cleave("#rrn", {
  blocks: [6, 7],
  delimiter: "-"
});

var phoneCleave = new Cleave("#phone", {
  phone: true,
  phoneRegionCode: "KR",
  delimiter: "-"
});

// Data Binding

var elements = [
  "title",
  "who",
  "when",
  "where",
  "content",
  "witness",
  "method",
  "grasp",
  "term",
  "lawyer"
];

function bindingData() {
  elements.forEach(el => {
    if (el === "grasp" || el === "term") {
      var value = $("input[name='" + el + "']:checked").val();
      $("div[name='" + el + "']").html(value);
    } else if (el === "content" || el === "witness" || el === "method") {
      var value = $("textarea[name='" + el + "']").val();
      $("div[name='" + el + "']").html(value);
    } else if (el === "lawyer") {
      var lawyerId = $("input[name='" + el + "']:checked").val();
      var lawyerEl = $("#" + lawyerId + " > label").html();
      $("#lawyer_confirm").html(lawyerEl);
    } else {
      var value = $("input[name='" + el + "']").val();
      $("div[name='" + el + "']").html(value);
    }
  });
}

// Address API

function execDaumPostcode() {
  new daum.Postcode({
    oncomplete: function (data) {
      var addr = "";

      if (data.userSelectedType === "R") addr = data.roadAddress;
      else addr = data.jibunAddress;

      document.getElementById("address").value = addr;
      document.getElementById("detailAddress").removeAttribute("readonly");
      document.getElementById("detailAddress").focus();
    }
  }).open();
}

// iamport SMS Authentication API

window.onload = function () {
  document.getElementById("step_" + page).style.display = "flex";
  lightIndex(page);
  manageButton();
  IMP.init("iamport");
};

function smsCertification() {
  console.log("Abc");
  IMP.certification({
      merchant_uid: "merchant_" + new Date().getTime() //본인인증과 연관된 가맹점 내부 주문번호가 있다면 넘겨주세요
    },
    function (rsp) {
      if (rsp.success) {
        // 인증성공
        console.log(rsp.imp_uid);
        console.log(rsp.merchant_uid);

        $.ajax({
          type: "POST",
          url: "/certifications/confirm",
          dataType: "json",
          data: {
            imp_uid: rsp.imp_uid
          }
        }).done(function (rsp) {
          // 이후 Business Logic 처리하시면 됩니다.
        });
      } else {
        // 인증취소 또는 인증실패
        var msg = "인증에 실패하였습니다.";
        msg += "에러내용 : " + rsp.error_msg;

        alert(msg);
      }
    }
  );
}