// 입력값 포맷 라이브러리 적용

var phoneCleave = new Cleave("#phone", {
  phone: true,
  phoneRegionCode: "KR",
  delimiter: "-"
});

window.onload = function () {
  document.querySelectorAll(".input_date").forEach(el => {
    new Cleave(el, {
      date: true,
      delimiter: "/",
      datePattern: ["Y", "m"]
    });
  });

  document.querySelectorAll(".input_count").forEach(el => {
    new Cleave(el, {
      numeral: true
    });
  });
};

// 변호사 자격사항 입력 폼 스크립트
lawyer_qual = []
//처음 들어올 때 보여주는 폼
var forms1 = [
  `
  <tr>
    <td>자격시험 및 횟수</td>
    <td>
      사법 시험 <input type="text" style="width: 100px" class="input_count" name="qual" required/> 회
    </td>
  </tr>
  <tr>
    <td>자격 취득년월일</td>
    <td><input type="date" name="qual" required/></td>
  </tr>
  <tr>
    <td>교육기관 및 기수</td>
    <td>
      사법연수원 <input type="text" style="width: 100px" class="input_count" name="qual" required/> 기
    </td>
  </tr>
  <tr>
    <td>교육기관 수료년월일</td>
    <td><input type="date" name="qual" required/></td>
  </tr>
  `,
  `
  <tr>
    <td>자격시험 및 횟수</td>
    <td>변호사 시험 <input type="text" style="width: 100px" class="input_count" name="qual" required/> 회</td>
  </tr>
  <tr>
    <td>자격 취득년월일</td>
    <td><input type="date" name="qual" required/></td>
  </tr>
  <tr>
    <td>교육기관 및 기수</td>
    <td>법학전문대학원 <input type="text" style="width: 100px" class="input_count" name="qual" required/> 기</td>
  </tr>
  <tr>
    <td>교육기관 수료년월일</td>
    <td><input type="date" name="qual" required/></td>
  </tr>
  <tr>
    <td>로스쿨</td>
    <td>
      <select name="qual">
        <option value="강원대학교">강원대학교</option>
        <option value="건국대학교">건국대학교</option>
        <option value="경북대학교">경북대학교</option>
        <option value="경희대학교">경희대학교</option>
        <option value="고려대학교">고려대학교</option>
        <option value="동아대학교">동아대학교</option>
        <option value="부산대학교">부산대학교</option>
        <option value="서강대학교">서강대학교</option>
        <option value="서울대학교">서울대학교</option>
        <option value="서울시립대학교">서울시립대학교</option>
        <option value="성균관대학교">성균관대학교</option>
        <option value="아주대학교">아주대학교</option>
        <option value="연세대학교">연세대학교</option>
        <option value="영남대학교">영남대학교</option>
        <option value="원광대학교">원광대학교</option>
        <option value="이화여자대학교">이화여자대학교</option>
        <option value="인하대학교">인하대학교</option>
        <option value="전남대학교">전남대학교</option>
        <option value="전북대학교">전북대학교</option>
        <option value="제주대학교">제주대학교</option>
        <option value="중앙대학교">중앙대학교</option>
        <option value="충남대학교">충남대학교</option>
        <option value="충북대학교">충북대학교</option>
        <option value="한국외국어대학교">한국외국어대학교</option>
        <option value="한양대학교">한양대학교</option>
      </select>
    </td>
  </tr>
  `,
  `
  <tr>
    <td>자격시험 및 횟수</td>
    <td class="input_horizontal">
      <div class="input_radio">
        <input type="radio" id="input_2_1" name="qual" value="사법" required/>
        <label for="input_2_1">사법 시험</label>
        <div class="check_radio"></div>
      </div>
      <div class="input_radio">
        <input type="radio" id="input_2_2" name="qual" value="변호사" required/>
        <label for="input_2_2">변호사 시험</label>
        <div class="check_radio"></div>
      </div>
      <input type="text" style="width: 100px" class="input_count" name="qual" required/>&nbsp;회
    </td>
  </tr>
  <tr>
    <td>자격 취득년월일</td>
    <td><input type="date" name="qual"/></td>
  </tr>
  <tr>
    <td>교육기관 및 기수</td>
    <td>
      사법연수원 <input type="text" style="width: 100px" class="input_count" name="qual" required/> 기
    </td>
  </tr>
  <tr>
    <td>교육기관 수료년월일</td>
    <td><input type="date" name="qual"/></td>
  </tr>
  `,
  `
  <tr>
    <td>자격시험 및 횟수</td>
    <td class="input_horizontal">
      <div class="input_radio">
        <input type="radio" id="input_2_1" name="qual" value="1" required/>
        <label for="input_2_1">사법 시험</label>
        <div class="check_radio"></div>
      </div>
      <div class="input_radio">
        <input type="radio" id="input_2_2" name="qual" value="1" required/>
        <label for="input_2_2">변호사 시험</label>
        <div class="check_radio"></div>
      </div>
      <input type="text" style="width: 100px" class="input_count" name="qual" required/>&nbsp;회
    </td>
  </tr>
  <tr>
    <td>자격 취득년월일</td>
    <td><input type="date" name="qual" required/></td>
  </tr>
  <tr>
    <td>교육기관 및 기수</td>
    <td>
      사법연수원 <input type="text" style="width: 100px" class="input_count" name="qual" required/> 기
    </td>
  </tr>
  <tr>
    <td>교육기관 수료년월일</td>
    <td><input type="date" name="qual" required/></td>
  </tr>
  `,
  `
  <tr>
    <td>자격시험 및 횟수</td>
    <td>
      군법무관 임용 시험 <input type="text" style="width: 100px" class="input_count" name="qual" required/> 회
    </td>
  </tr>
  <tr>
    <td>자격 취득년월일</td>
    <td><input type="date" name="qual" required/></td>
  </tr>
  <tr>
    <td>교육기관 및 기수</td>
    <td>
      군법무관실무고시 <input type="text" style="width: 100px" class="input_count" name="qual" required/> 기
    </td>
  </tr>
  <tr>
    <td>교육기관 수료년월일</td>
    <td><input type="date" name="qual" required/></td>
  </tr>
  `
];

//클릭할 때 바뀌는 폼
var forms2 = [
  `
  <tr>
    <td>자격시험 및 횟수</td>
    <td>
      사법 시험 <input type="text" style="width: 100px" class="input_count" name="qual" required/> 회
    </td>
  </tr>
  <tr>
    <td>자격 취득년월일</td>
    <td><input type="date" name="qual" required/></td>
  </tr>
  <tr>
    <td>교육기관 및 기수</td>
    <td>
      사법연수원 <input type="text" style="width: 100px" class="input_count" name="qual" required/> 기
    </td>
  </tr>
  <tr>
    <td>교육기관 수료년월일</td>
    <td><input type="date" name="qual" required/></td>
  </tr>
  `,
  `
  <tr>
    <td>자격시험 및 횟수</td>
    <td>변호사 시험 <input type="text" style="width: 100px" class="input_count" name="qual" required/> 회</td>
  </tr>
  <tr>
    <td>자격 취득년월일</td>
    <td><input type="date" name="qual" required/></td>
  </tr>
  <tr>
    <td>교육기관 및 기수</td>
    <td>법학전문대학원 <input type="text" style="width: 100px" class="input_count" name="qual" required/> 기</td>
  </tr>
  <tr>
    <td>교육기관 수료년월일</td>
    <td><input type="date" name="qual" required/></td>
  </tr>
  <tr>
    <td>로스쿨</td>
    <td>
      <select name="qual">
        <option value="강원대학교">강원대학교</option>
        <option value="건국대학교">건국대학교</option>
        <option value="경북대학교">경북대학교</option>
        <option value="경희대학교">경희대학교</option>
        <option value="고려대학교">고려대학교</option>
        <option value="동아대학교">동아대학교</option>
        <option value="부산대학교">부산대학교</option>
        <option value="서강대학교">서강대학교</option>
        <option value="서울대학교">서울대학교</option>
        <option value="서울시립대학교">서울시립대학교</option>
        <option value="성균관대학교">성균관대학교</option>
        <option value="아주대학교">아주대학교</option>
        <option value="연세대학교">연세대학교</option>
        <option value="영남대학교">영남대학교</option>
        <option value="원광대학교">원광대학교</option>
        <option value="이화여자대학교">이화여자대학교</option>
        <option value="인하대학교">인하대학교</option>
        <option value="전남대학교">전남대학교</option>
        <option value="전북대학교">전북대학교</option>
        <option value="제주대학교">제주대학교</option>
        <option value="중앙대학교">중앙대학교</option>
        <option value="충남대학교">충남대학교</option>
        <option value="충북대학교">충북대학교</option>
        <option value="한국외국어대학교">한국외국어대학교</option>
        <option value="한양대학교">한양대학교</option>
      </select>
    </td>
  </tr>
  `,
  `
  <tr>
    <td>자격시험 및 횟수</td>
    <td class="input_horizontal">
      <div class="input_radio">
        <input type="radio" id="input_2_1" name="qual" value="사법" required/>
        <label for="input_2_1">사법 시험</label>
        <div class="check_radio"></div>
      </div>
      <div class="input_radio">
        <input type="radio" id="input_2_2" name="qual" value="변호사" required/>
        <label for="input_2_2">변호사 시험</label>
        <div class="check_radio"></div>
      </div>
      <input type="text" style="width: 100px" class="input_count" name="qual" required/>&nbsp;회
    </td>
  </tr>
  <tr>
    <td>자격 취득년월일</td>
    <td><input type="date" name="qual"/></td>
  </tr>
  <tr>
    <td>교육기관 및 기수</td>
    <td>
      사법연수원 <input type="text" style="width: 100px" class="input_count" name="qual" required/> 기
    </td>
  </tr>
  <tr>
    <td>교육기관 수료년월일</td>
    <td><input type="date" name="qual"/></td>
  </tr>
  `,
  `
  <tr>
    <td>자격시험 및 횟수</td>
    <td class="input_horizontal">
      <div class="input_radio">
        <input type="radio" id="input_2_1" name="qual" value="1" required/>
        <label for="input_2_1">사법 시험</label>
        <div class="check_radio"></div>
      </div>
      <div class="input_radio">
        <input type="radio" id="input_2_2" name="qual" value="1" required/>
        <label for="input_2_2">변호사 시험</label>
        <div class="check_radio"></div>
      </div>
      <input type="text" style="width: 100px" class="input_count" name="qual" required/>&nbsp;회
    </td>
  </tr>
  <tr>
    <td>자격 취득년월일</td>
    <td><input type="date" name="qual" required/></td>
  </tr>
  <tr>
    <td>교육기관 및 기수</td>
    <td>
      사법연수원 <input type="text" style="width: 100px" class="input_count" name="qual" required/> 기
    </td>
  </tr>
  <tr>
    <td>교육기관 수료년월일</td>
    <td><input type="date" name="qual" required/></td>
  </tr>
  `,
  `
  <tr>
    <td>자격시험 및 횟수</td>
    <td>
      군법무관 임용 시험 <input type="text" style="width: 100px" class="input_count" name="qual" required/> 회
    </td>
  </tr>
  <tr>
    <td>자격 취득년월일</td>
    <td><input type="date" name="qual" required/></td>
  </tr>
  <tr>
    <td>교육기관 및 기수</td>
    <td>
      군법무관실무고시 <input type="text" style="width: 100px" class="input_count" name="qual" required/> 기
    </td>
  </tr>
  <tr>
    <td>교육기관 수료년월일</td>
    <td><input type="date" name="qual" required/></td>
  </tr>
  `
];
// 변호사 자격사항 입력 구분에 따라 다른 form


capacity = document.querySelector("#capacity");
document.querySelectorAll('input[name="qual_category"]').forEach(el => {
  if (el.checked) {
    capacity.innerHTML = forms1[el.value - 1];
  };
});

document.querySelectorAll('input[name="qual_category"]').forEach(el => {
  el.addEventListener("click", () => {
    capacity.innerHTML = forms2[el.value - 1];
  });
});


// 변호사 자격사항 및 전문분야 한 string 으로 합쳐주기
function lawyerSubmit() {
  form = document.querySelector("#lawyerForm");

  var specialty = function () {
    var specialty_list = [];
    form.fields.forEach(el => {
      if (el.checked) specialty_list.push(el.value);
    });
    return specialty_list.join("/");
  };

  var qual_func = function () {
    var qual_list = [];
    form.qual.forEach(el => {
      qual_list.push(el.value);
    });
    return qual_list.join("/");
  };

  // document.querySelector('input[name="merged_specialty"]').value = specialty();
  document.querySelector('input[name="merged_qual"]').value = qual_func();



  // js submit 은 required 가 실행이 안되서 다음과 같이 button을 클릭하도록
  document.querySelector("#real_submit").click();
}