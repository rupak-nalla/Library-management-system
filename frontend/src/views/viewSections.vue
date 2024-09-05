<script setup>
import { onMounted,ref } from 'vue'; 
import router from '@/router';
const sectionsData=ref([{
     'Sname':'secction name',
     'Sid':0
}])


const role=ref('');
async function fetchSections() {
     const token = localStorage.getItem('token');
     const res= await fetch("http://localhost:8080/api/sections",{
          method:"GET",
          headers: {
               'Authorization': `Bearer ${token}`,
               'Content-Type':'application/json'
          }
     });
     if (res.status == 200) {
  
  let result = await res.json();
  console.log(result)
  if (result['secDetails'].length > 0) {
    sectionsData.value=result['secDetails']
    
  } else {
    console.log('No books found');
  }
  role.value=result['role']
} else if (res.status == 401) {
  localStorage.removeItem('token');
  router.push('/LibrarianLogin');
}
}

onMounted( async () => {
     await fetchSections();
     
})


function viewSection(Sid) {
     router.push(`/section/${Sid}`)
}
function editSection(Sid) {
     router.push(`/section/${Sid}/edit`)
}
async function deleteSection(Sid){
     const token = localStorage.getItem('token');
     const b={
          "sid":Sid
     }
     const res= await fetch("http://localhost:8080/api/sections",{
          method:"DELETE",
          headers: {
               'Authorization': `Bearer ${token}`,
               'Content-Type':'application/json'
          },
          body:JSON.stringify(b)
     });
     if (res.status==200) {
          alert("deleted succussfully");
          router.go(0)
     }
     else{
          alert("not deleted")
     }
}

const searched=ref(false);
const searchResult=ref(false);
const searchRes=ref([])
function search() {
     const searchVal=document.getElementById('search-value').value;
     searchRes.value=[]
     console.log(searchVal);
     searched.value=true;
     let res=[]
     console.log(sectionsData)
     for(let i =0;i<sectionsData.value.length;i+=1){
          console.log("in loop")
          console.log(sectionsData.value[i].Sname,searchVal)
          if(sectionsData.value[i].Sname.includes(searchVal)){
               res.push(sectionsData.value[i])
          }
          
     }
     console.log(res)
     if(res.length==0){
          searchResult.value=false;
     }
     else{
          searchResult.value=true;
          searchRes.value=res
          console.log(searchRes);
     }
}


</script>
<template>
     <div id="main" class="row">
          <div id="side-bar" class="col-2">
               <ul v-if="role=='lib'" id="side-bar-list" style="position: sticky;">
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
               <ul v-if="role=='user'" id="side-bar-list" style="position: sticky;">
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
          <div class="col" style="padding:10px;color: white;">
               <div style="display: flex;justify-content: space-between;align-items: center;">
                    <h1>Sections</h1>
                    <div v-if="role=='lib'">
                         <button class="btn btn-primary" @click="()=>{router.push('/createSection')}">Add Section</button>
                    </div>
               </div>
               <div class="row">
                    <div style="">
                              <div class="input-group mb-3" style="width: 30%;">
                                   <input type="text" id="search-value" class="form-control" placeholder="search" aria-label="Recipient's username" aria-describedby="basic-addon2">
                                   <span class="input-group-text" id="basic-addon2" @click="search()">
                                        <a style="color: black; text-decoration: none;">
                                             <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
                                                  <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
                                             </svg>
                                        </a>
                                        

                                   </span>
                              </div>
                         </div>
               </div>
               <div class="row">
                    <div v-if="searched">
                         <h3>Search Result</h3>
                         <div v-if="searchResult">
                              <div class="card" v-for="i in searchRes.length" style="margin: 10px;">
                                   <div class="card-body" style="display: flex;justify-content: space-between;align-items: center;">
                                        <div class="">
                                             <h3>{{ searchRes[i-1].Sname }}</h3>
                                        </div>
                                        <div class="float:left;">
                                             <button class="btn btn-primary" style="margin: 5px;" @click="viewSection(searchRes[i-1].Sid)">View</button>
                                                  
                                             <div v-if="role=='lib'">

                                                  <button class="btn btn-primary"style="margin: 5px;" @click="editSection(searchRes[i-1].Sid)">Edit</button>
                                                  <button class="btn btn-danger" style="margin: 5px;" @click="deleteSection(searchRes[i-1].Sid)">Delete</button>
                                             </div>
                                             
                                        </div>
                                   </div>
                              </div>
                         </div>
                         <div v-else>
                              <h3>No matching Sections found</h3>
                         </div>
                         <hr>
                    </div>
               </div>
               <div class="card" v-for="i in sectionsData.length" style="margin: 10px;">
                    <div class="card-body" style="display: flex;justify-content: space-between;align-items: center;">
                         <div class="">
                              <h3>{{ sectionsData[i-1].Sname }}</h3>
                         </div>
                         <div class="float:left;">
                              <button class="btn btn-primary" style="margin: 5px;" @click="viewSection(sectionsData[i-1].Sid)">View</button>
                                   
                              <div v-if="role=='lib'">

                                   <button class="btn btn-primary"style="margin: 5px;" @click="editSection(sectionsData[i-1].Sid)">Edit</button>
                                   <button class="btn btn-danger" style="margin: 5px;" @click="deleteSection(sectionsData[i-1].Sid)">Delete</button>
                              </div>
                              
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