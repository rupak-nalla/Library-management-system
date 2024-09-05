<script setup>
import { ref,onMounted } from 'vue'
import router from '@/router';
import { useRoute } from 'vue-router';

const route = useRoute();
const secData=ref({
     'userRole':'user',
     'SName':'sectionName',
     'books':[{
          'Bid':0,
          'BName':'BookName'
     }]
})
const mybooks=ref([
     {
      "Bid": 0,
      "Name": "null",
      "AuthorName": "null",
      "AvgRating": 0,
      "CoverPath":'../assets/book-cover.jpg'
    }
])
const booksData=ref([[{
     'Bid':0,
     'Name':'BookName',
     'AuthorName':'AuthorName',
     'AvgRating':0
}]])
const sid=route.params.sid;
const role=ref('');
async function fetchSectionData() {
     const token = localStorage.getItem('token');
     const res= await fetch(`http://localhost:8080/api/getSection/${sid}`,{
          method:"GET",
          headers: {
               'Authorization': `Bearer ${token}`,
               'Content-Type':'application/json'
          }
          
     });
     if (res.status == 200) {
          secData.value=await res.json();
          role.value=secData['userRole'];
          console.log(secData)
     }
     else if (res.status == 401) {
          localStorage.removeItem('token');
          router.push('/LibrarianLogin');
     }
}
async function SendRequest(Bid) {
     const token = localStorage.getItem('token');
     const b={
          "Bid":Bid
     }
     const res= await fetch("http://localhost:8080/api/BookReq",{
          method:"POST",
          headers: {
               'Authorization': `Bearer ${token}`,
               'Content-Type':'application/json'
          },
          body:JSON.stringify(b)
     });
     if (res.status==200) { 
          let result = await res.json();
          alert(result.msg);
     }else if(res.status==409){
          const data = await res.text();
          alert(data);
          
     }
}

async function RemoveBook(Bid){
     const token = localStorage.getItem('token');
     const b={
          "Bid":Bid
     }
     const res= await fetch(`http://localhost:8080/api/getSection/${sid}`,{
          method:"DELETE",
          headers: {
               'Authorization': `Bearer ${token}`,
               'Content-Type':'application/json'
          },
          body:JSON.stringify(b)
     });
     if (res.status==200) { 
          let result = await res.json();
          alert(result.msg);
          router.go(0)
     }else if(res.status==409){
          const data = await res.text();
          alert(data);
          
     }
}



async function fetchMyBooks(){
     const token = localStorage.getItem('token');
     const res= await fetch("http://localhost:8080/api/booksIssued",{
          method:"GET",
          headers: {
               'Authorization': `Bearer ${token}`,
               'Content-Type':'application/json'
          }
     });
     if (res.status==200) {
          const result=await res.json()
          let temp=result['Books']
          for (let i = 0; i < temp.length; i++) {
               const element = temp[i];
               element.CoverPath=convertPath(element.CoverPath)
          }
          mybooks.value=temp
     }
     else if(res.status==401){
          localStorage.removeItem('token')
          router.push('/');
     }
}
onMounted(async()=>{
     fetchSectionData();
     if (role=='user') {
          fetchMyBooks();
          fetchBooks();
     }
})



</script>
<template>
     <div id="main" class="row" >
          <div id="side-bar" class="col-2">
               <ul v-if="secData['userRole']=='lib'" id="side-bar-list" style="position: sticky;">
                    <li>
                         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-house-door-fill" viewBox="0 0 16 16">
                              <path d="M6.5 14.5v-3.505c0-.245.25-.495.5-.495h2c.25 0 .5.25.5.5v3.5a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5"/>
                         </svg>
                         
                         <a href="/LibrarianDashBoard"style="margin-left: 5px;color: white;text-decoration: none;">Home</a></li>  
                    <li>
                         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                              <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                              <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                         </svg>

                         <a href="/viewBooks" style="margin-left: 5px; color: white;text-decoration: none;">View Books</a>
                    </li> 
                    <li>
                         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-text-fill" viewBox="0 0 16 16">
                              <path d="M12 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2M5 4h6a.5.5 0 0 1 0 1H5a.5.5 0 0 1 0-1m-.5 2.5A.5.5 0 0 1 5 6h6a.5.5 0 0 1 0 1H5a.5.5 0 0 1-.5-.5M5 8h6a.5.5 0 0 1 0 1H5a.5.5 0 0 1 0-1m0 2h3a.5.5 0 0 1 0 1H5a.5.5 0 0 1 0-1"/>
                         </svg>

                         <a href="/viewSections" style="margin-left: 5px;color: white;text-decoration: none;">View Sections</a>
                    </li>
                    <li>
                         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-text-fill" viewBox="0 0 16 16">
                              <path d="M12 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2M5 4h6a.5.5 0 0 1 0 1H5a.5.5 0 0 1 0-1m-.5 2.5A.5.5 0 0 1 5 6h6a.5.5 0 0 1 0 1H5a.5.5 0 0 1-.5-.5M5 8h6a.5.5 0 0 1 0 1H5a.5.5 0 0 1 0-1m0 2h3a.5.5 0 0 1 0 1H5a.5.5 0 0 1 0-1"/>
                         </svg>

                         <a href="/booksissued" style="margin-left: 5px;color: white;text-decoration: none;">View books issued</a>
                    </li>
                    <li>
                         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-box-arrow-left" viewBox="0 0 16 16">
                              <path fill-rule="evenodd" d="M6 12.5a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5v-9a.5.5 0 0 0-.5-.5h-8a.5.5 0 0 0-.5.5v2a.5.5 0 0 1-1 0v-2A1.5 1.5 0 0 1 6.5 2h8A1.5 1.5 0 0 1 16 3.5v9a1.5 1.5 0 0 1-1.5 1.5h-8A1.5 1.5 0 0 1 5 12.5v-2a.5.5 0 0 1 1 0z"/>
                              <path fill-rule="evenodd" d="M.146 8.354a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L1.707 7.5H10.5a.5.5 0 0 1 0 1H1.707l2.147 2.146a.5.5 0 0 1-.708.708z"/>
                         </svg>
                         <a href="/LibrarianLogin" style="margin-left: 5px;color: white;text-decoration: none;">Logout</a>
                    </li> 
                    
               </ul>
               <ul v-if="secData['userRole']=='user'" id="side-bar-list" style="position: sticky;">
                    <li>
                         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-house-door-fill" viewBox="0 0 16 16">
                              <path d="M6.5 14.5v-3.505c0-.245.25-.495.5-.495h2c.25 0 .5.25.5.5v3.5a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5"/>
                         </svg>

                         <a href="/Home"style="margin-left: 5px;color: white;text-decoration: none;">Home</a></li>  
                    <li>
                         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                              <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                              <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                         </svg>

                         <a href="/Profile" style="margin-left: 5px; color: white;text-decoration: none;">Profile</a>
                    </li> 
                    <li>
                         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-text-fill" viewBox="0 0 16 16">
                              <path d="M12 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2M5 4h6a.5.5 0 0 1 0 1H5a.5.5 0 0 1 0-1m-.5 2.5A.5.5 0 0 1 5 6h6a.5.5 0 0 1 0 1H5a.5.5 0 0 1-.5-.5M5 8h6a.5.5 0 0 1 0 1H5a.5.5 0 0 1 0-1m0 2h3a.5.5 0 0 1 0 1H5a.5.5 0 0 1 0-1"/>
                         </svg>

                         <a href="/Requests" style="margin-left: 5px;color: white;text-decoration: none;">My Requests</a>
                    </li>
                    <li>
                         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-text-fill" viewBox="0 0 16 16">
                              <path d="M12 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2M5 4h6a.5.5 0 0 1 0 1H5a.5.5 0 0 1 0-1m-.5 2.5A.5.5 0 0 1 5 6h6a.5.5 0 0 1 0 1H5a.5.5 0 0 1-.5-.5M5 8h6a.5.5 0 0 1 0 1H5a.5.5 0 0 1 0-1m0 2h3a.5.5 0 0 1 0 1H5a.5.5 0 0 1 0-1"/>
                         </svg>

                         <a href="/viewSections" style="margin-left: 5px;color: white;text-decoration: none;">View Sections</a>
                    </li>
                    <li>
                         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-box-arrow-left" viewBox="0 0 16 16">
                              <path fill-rule="evenodd" d="M6 12.5a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5v-9a.5.5 0 0 0-.5-.5h-8a.5.5 0 0 0-.5.5v2a.5.5 0 0 1-1 0v-2A1.5 1.5 0 0 1 6.5 2h8A1.5 1.5 0 0 1 16 3.5v9a1.5 1.5 0 0 1-1.5 1.5h-8A1.5 1.5 0 0 1 5 12.5v-2a.5.5 0 0 1 1 0z"/>
                              <path fill-rule="evenodd" d="M.146 8.354a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L1.707 7.5H10.5a.5.5 0 0 1 0 1H1.707l2.147 2.146a.5.5 0 0 1-.708.708z"/>
                         </svg>
                         <a href="/" style="margin-left: 5px;color: white;text-decoration: none;">Logout</a>
                    </li> 
                    
               </ul>
          </div>
          <div class="col" style="color: white;margin: 10px;" >
               <div style="display: flex;justify-content: space-between;">
                    <h3 style="color: white;">{{ secData['SName'] }}</h3>
                    <button v-if="secData['userRole']=='lib'" class="btn btn-primary" @click="()=>{router.push(`/section/${sid}/edit`)}">edit Book</button>
               </div>
               <div class="card" v-for="i in secData['books'].length" style="margin: 10px;">
                    <div class="card-body" style="display: flex;justify-content: space-between;">
                         <h3>{{secData['books'][i-1].Name}}</h3>
                         <div v-if="secData['userRole']=='lib'">
                              <button class="btn btn-danger" @click="RemoveBook(secData['books'][i-1].Bid)">Remove</button>
                         </div>
                         <div v-else>
                              <button class="btn btn-primary" @click="SendRequest(secData['books'][i-1].Bid)" >Request</button>
                         </div>
                    </div>
               </div>
          </div>
     </div>
</template>
<style scoped>
/* #main{
  background-color: #eceaea;
  height: 100%;
  min-height: 500px;
} */
#side-bar-list{
     list-style-type: none;
     font-size: 20px;

}
@font-face {
    font-family: 'CustomFont';
    src: url('../assets/font/ClashDisplay_Complete/Fonts/TTF/ClashDisplay-Variable.ttf') format('truetype'); /* Adjust the path as necessary */
}
#main{
  /* background-color: rgb(30, 30,30); */
  background-color: rgb(15, 15, 15);
  height: 100%;
  min-height: 500px;
  font-family: 'CustomFont';
}
#side-bar-list{
     list-style-type: none;
     font-size: 20px;

}
#side-bar{
     background-color: rgb(11, 11, 11);
     display: flex;
     justify-content: center;
     padding-top: 100px;
     width: 250px;
}
ul li{
     padding: 20px;
}
#login-card{
  width: 300px;
  min-height: 300px;
  height: fit-content;
}
.card{
     background-color:rgb(33, 33, 33);
     color:white;
     border-radius: 18px;
}
#inner-card{
     background-color: rgb(23, 23, 23);
}
</style>