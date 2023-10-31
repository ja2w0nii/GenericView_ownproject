![header](https://capsule-render.vercel.app/api?type=waving&color=auto&height=300&section=header&text=OWN%20Project&fontSize=90)

# 💻 Django GenericView Project
### Django GenericView로 구현한 커뮤니티 서비스

</br>

## 🛠 Stacks
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white"> <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=Redis&logoColor=white"> <img src="https://img.shields.io/badge/YOLO-00FFFF?style=for-the-badge&logo=YOLO&logoColor=white"> <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=HTML5&logoColor=white"> <img src="https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=CSS3&logoColor=white">

</br>

## 🌱 Contributor
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/ja2w0nii">
        <sub><b>김재원</b></sub></a><br />
        <sub><b>Developer</b></sub></a><br />    
   <sub><b></b></sub></a><br/>
        <a href="https://github.com/ja2w0nii" title="Code">💻</a>
    </td>
  </tr>
</table>

</br>

## 🌠 Service

### 회원 기능
: 회원 가입/탈퇴, 로그인/로그아웃, 프로필 조회/수정, 팔로우 등록/취소

### 게시글/댓글을 통한 커뮤니티
: 게시글/댓글 CRUD, 좋아요 기능, 검색 기능

### 실시간 채팅
: 회원 간 실시간 채팅(Django Channels & Redis)

</br>

## 📂 Structure

```
genericview
├─ chat                             // live chatting app
│  ├─ templates
│  ├─ urls.py
│  ├─ views.py
├─ detection                        // AI detection app
│  ├─ templates
│  ├─ urls.py
│  ├─ views.py
│  ├─ yolov8.py
├─ genericview                      // project 
│  ├─ settings.py                   // setting
│  ├─ urls.py                       // base url
├─ posts                            // posting app
│  ├─ templates
│  ├─ urls.py
│  ├─ views.py
├─ users                            // user app
│  ├─ templates
│  ├─ urls.py
│  ├─ views.py
├─ **manage.py**                    // main
└─ requirements.txt
```
