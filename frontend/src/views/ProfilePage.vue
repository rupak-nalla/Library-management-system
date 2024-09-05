<script setup>
import router from '@/router';
import { ref,onMounted } from 'vue';
const edit=ref(false);
function EditProfile() {
     edit.value=!edit.value;
}
async function HandleSubmit() {
     const editUserName=document.getElementById('editUserName').value;
     const editEmail=document.getElementById('editEmail').value;
     const fileInput = document.getElementById('formFile');
     console.log(editUserName);
     console.log(editEmail);
     let filePresent=true
     if (fileInput.files.length === 0) {
          filePresent=false
     }
     const file = fileInput.files[0];
     const formData=new FormData();
     
     formData.append('editUserName',editUserName);
     formData.append('editEmail',editEmail);
     console.log(formData.entries());
     for (let [key, value] of formData.entries()) {
        console.log(key, value);
      }
     if (filePresent){
          formData.append('file', file);
     }
     
     const token = localStorage.getItem('token');
     console.log(token);
     const res= await fetch("http://localhost:8080/api/user",{
        method:"PUT",
        headers: {
          'Authorization': `Bearer ${token}`
          
        },
        redirect:"manual",
        body:formData
      })
      
      if (res.status==200) {
        console.log(res);
        alert('Success');
        router.go(0);

      }
      else if(res.status==409){
        
        let result=await res.text()
        console.log(result);
        alert(result);
      }
      else if(res.status==404){
          let result=await res.text()
          console.log(result);
          alert(result);
      }

}
const userdata=ref({
     'id':0,
     'Name':'username',
     'Email':'example@gmail.com',
     'ProfileImg':'../assets/images/no-profile.jpeg'
});
function convertPath(absolutePath) {
      // Replace backslashes with forward slashes
      const normalizedPath = absolutePath.replace(/\\/g, '/');
      
      // Split the path into segments
      const pathSegments = normalizedPath.split('/');
      
      // Find the index of the target folder (assuming 'frontend' is the target folder)
      const targetIndex = pathSegments.indexOf('src');

      // If the target folder is found, construct the relative path
      let relativePath;
      if (targetIndex !== -1) {
        const relativeSegments = pathSegments.slice(targetIndex);
        relativePath = `../${relativeSegments.join('/')}`;
      } else {
        relativePath = 'Target folder not found in the path';
      }
      console.log(relativePath)
      return relativePath
    }
async function fetchUserData(){
     
     const token = localStorage.getItem('token');
     const res= await fetch("http://localhost:8080/api/user",{
          method:"GET",
          headers: {
               'Authorization': `Bearer ${token}`,
               'Content-Type':'application/json'
          }
     });
     if (res.status==200) {
          userdata.value=await res.json();
          if(userdata.value.ProfileImg){
               userdata.value.ProfileImg=convertPath(userdata.value.ProfileImg)
          }
          console.log(userdata.value);
     }


}
onMounted(async () => {
     await fetchUserData();
})
</script>
<template>
     <div id="main" class="row">
          <div id="side-bar" class="col-2">
               <ul id="side-bar-list" style="position: sticky;">
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
          <div class="col">
               <div style="margin: 20px 10px 10px 20px;">
                    <h3 style="font-size: 25px;">Profile</h3>
                    <div v-if="edit">
                         
                              <div class="row" style="display:flex;justify-content: center;margin-bottom: 10px;">
                                   <img :src="userdata.ProfileImg" style="padding: 0px; aspect-ratio: 1/1;width: 100px; border-radius: 50%;">
                              </div>
                              <div class="row">
                                   <h4>User Name</h4>
                                   <div class="mb-3">
                                        <input type="text" id="editUserName" aria-describedby="helpId" class="form-control" style="width:250px;" :value="userdata.Name" placeholder="username" required>
                                   </div>
                                   <br>
                                   <h4>Email</h4>
                                   <div class="mb-3">
                                        <input type="email"  aria-describedby="helpId" class="form-control" style="width:250px;" id="editEmail" :value="userdata.Email" placeholder="example@gmail.com" required>
                                   </div>
                                   <div class="mb-3">
                                        <h4 for="formFile" class="form-label">Upload Profile Image</h4>
                                        <input class="form-control" type="file" style="width:250px;" id="formFile">
                                   </div>
                                   <div style="display: flex;">
                                        <button class="btn btn-primary" @click="HandleSubmit">Submit</button>
                                        <button class="btn btn-primary" @click="EditProfile">Back</button>
                                   </div>
                              </div>
                    </div>
                    <div v-else>
                         <div class="row" style="display:flex;justify-content: center;margin-bottom: 10px;">
                              <img :src="userdata.ProfileImg" style="padding: 0px; aspect-ratio: 1/1;width: 100px; border-radius: 50%;">
                         </div>
                         <div class="row">
                              <h4>User Name</h4>
                              <h5 id="val">{{ userdata.Name }}</h5>
                              <br>
                              <h4>Email</h4>
                              <h5 id="val">{{ userdata.Email }}</h5>
                              
                              <div style="display: flex;">
                                        
                                   <button class="btn btn-primary" @click="EditProfile">Edit</button>
                              </div>
                         </div>   
                    </div>
               </div>
               
          </div>
     </div>
</template>
<style scoped>
     @font-face {
    font-family: 'CustomFont';
    src: url('../assets/font/ClashDisplay_Complete/Fonts/TTF/ClashDisplay-Variable.ttf') format('truetype'); /* Adjust the path as necessary */
}
#main{
     background-color: rgb(15, 15, 15);
     height: 100%;
     min-height: 500px;
     font-family: 'CustomFont';
     color:white;
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
#val{
     color: rgb(132, 132, 132);
}
</style>