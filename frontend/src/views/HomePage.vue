<script setup>
import router from '@/router';
import {ref,onMounted} from 'vue'

const userdata=ref({
     'id':0,
     'Name':'username',
     'Email':'example@gmail.com',
     'ProfileImg':'../assets/images/no-profile.jpeg'
});
const booksData=ref([[{
     'Bid':0,
     'Name':'BookName',
     'AuthorName':'AuthorName',
     'AvgRating':0
}]])
function convertPath(absolutePath) {
  // Replace backslashes with forward slashes
  const normalizedPath = absolutePath.replace(/\\/g, '/');

  // Split the path into segments
  const pathSegments = normalizedPath.split('/');

  // Find the index of the last segment (the file name)
  const fileNameIndex = pathSegments.length - 1;

  // Construct the relative path by joining the segments from the 'src' folder onwards
  const relativeSegments = pathSegments.slice(pathSegments.indexOf('src'));
  const relativePath = `../${relativeSegments.join('/')}`;

  return relativePath;
}
// fetches user data
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
          
          console.log(userdata);
     }
     else if(res.status==401){
          localStorage.removeItem('token')
          router.push('/');
     }


}
// fetches all books
async function fetchBooks() {
     const token = localStorage.getItem('token');
     const res= await fetch("http://localhost:8080/api/books",{
          method:"GET",
          headers: {
               'Authorization': `Bearer ${token}`,
               'Content-Type':'application/json'
          }
     });
     if (res.status==200) {
          let temp=[];
          let temp2=[]
          let result=await res.json();
          for (let i = 0; i < result.length; i+=2) {
               temp.push(result[i]);
               temp.push(result[i+1]);
               temp2.push(temp);
               temp=[];
          }
          for (let i = 0; i < temp2.length; i++) {
               for (let j = 0; j < temp2[i].length; j++) {
                    if (temp2[i][j]) {
                         const element = temp2[i][j];
                         element.CoverPath = convertPath(element.CoverPath);
                    }
               }
          }
          booksData.value=temp2;
          console.log(booksData);
     }
     else if(res.status==401){
          localStorage.removeItem('token')
          router.push('/');
     }
}
const mybooks=ref([
     {
      "Bid": 0,
      "Name": "null",
      "AuthorName": "null",
      "AvgRating": 0,
      "CoverPath":'../assets/book-cover.jpg',
      'Content':'Content'
    }
])
// fetches books issued to the user
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
onMounted(async () => {
     await fetchUserData();
     await fetchBooks();
     await fetchMyBooks();
})
// requests a book 
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


// returns book
async function RevokeBook(i){
     const token = localStorage.getItem('token');
     const b={
          'Bid':i
     }
     const res= await fetch("http://localhost:8080/api/booksIssued",{
          method:"DELETE",
          headers: {
               'Authorization': `Bearer ${token}`,
               'Content-Type':'application/json'
          },
          body:JSON.stringify(b)
     });
     if (res.status==200) {
          const result=await res.json()
          alert(result.msg);
          router.go(0);
     }
     else if(res.status==401){
          localStorage.removeItem('token')
          router.push('/');
     }
}

var rating;
// rating of books
async function handleRating(Bid){
     const token = localStorage.getItem('token');
     const rate = rating;
     const b={
          "Rating":rate,
          "Bid":Bid
     }
     console.log('In Handle Rating')
     const res= await fetch("http://localhost:8080/api/Rating",{
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
          router.go(0);
     }else if(res.status==409){
          const data = await res.text();
          alert(data);
          
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
     console.log(booksData)
     for(let i =0;i<booksData.value.length;i+=1){
          console.log("in loop")
          console.log(booksData.value[i][0].Name,searchVal)
          if(booksData.value[i][0].Name.includes(searchVal)){
               res.push(booksData.value[i][0])
          }
          else if (booksData.value[i][1] && booksData.value[i][1].Name.includes(searchVal)) {
               res.push(booksData.value[i][1])
          }
     }
     console.log(res)
     if(res.length==0){
          searchResult.value=false;
     }
     else{
          searchResult.value=true;
          let temp=[];
          let temp2=[]
          let result=res;
          for (let i = 0; i < result.length; i+=2) {
               temp.push(result[i]);
               temp.push(result[i+1]);
               temp2.push(temp);
               temp=[];
          }
          for (let i = 0; i < temp2.length; i++) {
               for (let j = 0; j < temp2[i].length; j++) {
                    if (temp2[i][j]) {
                         const element = temp2[i][j];
                         element.CoverPath = convertPath(element.CoverPath);
                    }
               }
          }
          searchRes.value=temp2;
          console.log(searchRes);
     }
}


</script>

<template>
     
     <div id="main" class="row" style="color: white;">
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
          <div class="col" style="padding: 20px;">
               
               <h3>{{ userdata.Name }}'s Books</h3>
               <div class="row" style="display: flex;" v-if="mybooks.length>0">
                    <div class="" v-for="i in mybooks.length" style="width: calc(100%/5);">
                         <div class="card">
                              <img :src="mybooks[i-1].CoverPath" class="card-img-top" alt="...">

                              <div class="card-body">
                                   <h5>{{ mybooks[i-1].Name }}</h5>
                                   <p v-if="mybooks[i-1].AvgRating>0"><strong>Rating</strong>: {{ mybooks[i-1].AvgRating }}</p>
                                   <p v-else><strong>Rating</strong>: N/A</p>
                                   
                                   <p><strong>Author</strong>: {{ mybooks[i-1].AuthorName }}</p>
                                   <div style="display:flex; justify-content: left;">
                                        <button class="btn btn-primary" style="margin-right:5px;" data-bs-toggle="modal" :data-bs-target="`#book-modal-${mybooks[i-1].Bid}`">View</button>
                                        <!-- Modal -->
                                        <div style="backdrop-filter: blur(55px);" class="modal fade" :id="`book-modal-${ mybooks[i-1].Bid }`" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                             <div class="modal-dialog">
                                                  <div class="modal-content">
                                                       <div class="modal-header" style="color: white;background-color:rgb(33, 33, 33);border: 0px;">
                                                            <h1 class="modal-title fs-5" id="exampleModalLabel">{{ mybooks[i-1].Name }}</h1>
                                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                       </div>
                                                       <div class="modal-body" style="color: white;background-color:rgb(33, 33, 33)">
                                                            <h3>Author Name:{{ mybooks[i-1].AuthorName }}</h3>
                                                            <h3>Content</h3>
                                                            <p>{{ mybooks[i-1].Content }}</p>
                                                            <form>
                                                                 <input id="`Rating-${mybook[i-1].Bid}`" @change="(e)=>{rating=e.target.value;}" class="form-control" type="number" max="5" placeholder="Rate" aria-label="default input example">
                                                                 <button type="submit" @click="(e)=>{e.preventDefault();handleRating(mybooks[i-1].Bid);}" class="btn btn-primary">Rate</button>
                                                            </form>
                                                       </div>
                                                       <div class="modal-footer" style="color: white;background-color:rgb(33, 33, 33);border: 0px;">
                                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                                       </div>
                                                  </div>
                                             </div>
                                        </div>
                                        
                                        <button class="btn btn-primary" @click="RevokeBook(mybooks[i-1].Bid)">Return</button>
                                   </div>
                              </div>
                         </div>
                    </div>
                    
               </div>
               <div class="row" v-else>
                    <h6>No books to show</h6>
               </div>
               <!-- second row -->
               <div class="row">
                    <div class="row" style="display: flex;">
                         <h3>Books</h3>
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

                    <div v-if="searched" id="seach-results">
                         <div v-if="searchResult">
                              <h3>Search Results</h3>
                              <div class="row" v-for="i in  searchRes.length">
                                   <div class="col">
                                        <div class="card mb-3" style="max-width: 540px;">
                                             <div class="row g-0">
                                                  <div class="col-md-4">
                                                       <img :src="searchRes[i-1][0].CoverPath" class="img-fluid rounded-start" alt="...">
                                                  </div>
                                                  <div class="col-md-8">
                                                       <div class="card-body">
                                                            <h5 class="card-title">{{ searchRes[i-1][0].Name }}</h5>
                                                            <p class="card-text">
                                                                 <strong>Author</strong>:{{ searchRes[i-1][0].AuthorName }}<br>
                                                            </p>
                                                            
                                                            <button v-if="mybooks.length<5" class="btn btn-primary" @click="SendRequest(searchRes[i-1][0].Bid)">Request Book</button>
                                                            <div v-else>
                                                                 <p>Books limit Reached</p>
                                                            </div>
                                                       </div>
                                                  </div>
                                             </div>
                                        </div>
                                   </div>
                                   <div class="col">
                                        <div v-if="searchRes[i-1][1]" class="card mb-3" style="max-width: 540px;">
                                             <div class="row g-0">
                                                  <div class="col-md-4">
                                                       <img :src="searchRes[i-1][1].CoverPath" class="img-fluid rounded-start" alt="...">
                                                  </div>
                                                  <div class="col-md-8">
                                                       <div class="card-body">
                                                            <h5 class="card-title">{{ searchRes[i-1][1].Name }}</h5>
                                                            <p class="card-text">
                                                                 <strong>Author</strong>: {{ searchRes[i-1][1].AuthorName }}<br>
                                                            </p>
                                                            <button v-if="mybooks.length<5" class="btn btn-primary" @click="SendRequest(searchRes[i-1][1].Bid)">Request Book</button>
                                                            <div v-else>
                                                                 <p>Books limit Reached</p>
                                                            </div>
                                                       </div>
                                                  </div>
                                             </div>
                                        </div>
                                   </div>
                              </div>
                         </div>
                         <div v-else>
                              <h3>No matching Books found</h3>

                         </div>
                         <hr>
                    </div>

                    <!-- display all books -->
                    <div class="row" v-for="i in  booksData.length">
                         <div class="col">
                              <div class="card mb-3" style="max-width: 540px;">
                                   <div class="row g-0">
                                        <div class="col-md-4">
                                             <img :src="booksData[i-1][0].CoverPath" class="img-fluid rounded-start" alt="...">
                                        </div>
                                        <div class="col-md-8">
                                             <div class="card-body">
                                                  <h5 class="card-title">{{ booksData[i-1][0].Name }}</h5>
                                                  <p class="card-text">
                                                       <strong>Author</strong>:{{ booksData[i-1][0].AuthorName }}<br>
                                                  </p>
                                                  
                                                  <button v-if="mybooks.length<5" class="btn btn-primary" @click="SendRequest(booksData[i-1][0].Bid)">Request Book</button>
                                                  <div v-else>
                                                       <p>Books limit Reached</p>
                                                  </div>
                                             </div>
                                        </div>
                                   </div>
                              </div>
                         </div>
                         <div class="col">
                              <div v-if="booksData[i-1][1]" class="card mb-3" style="max-width: 540px;">
                                   <div class="row g-0">
                                        <div class="col-md-4">
                                             <img :src="booksData[i-1][1].CoverPath" class="img-fluid rounded-start" alt="...">
                                        </div>
                                        <div class="col-md-8">
                                             <div class="card-body">
                                                  <h5 class="card-title">{{ booksData[i-1][1].Name }}</h5>
                                                  <p class="card-text">
                                                       <strong>Author</strong>: {{ booksData[i-1][1].AuthorName }}<br>
                                                  </p>
                                                  <button v-if="mybooks.length<5" class="btn btn-primary" @click="SendRequest(booksData[i-1][1].Bid)">Request Book</button>
                                                  <div v-else>
                                                       <p>Books limit Reached</p>
                                                  </div>
                                             </div>
                                        </div>
                                   </div>
                              </div>
                         </div>
                    </div>
               </div>
          </div>
     </div>
</template>

<style scoped>

#side-bar{
     background-color: rgb(11, 11, 11);
     display: flex;
     justify-content: center;
     padding-top: 100px;
     width: 250px;
}
#login-card{
  width: 300px;
  min-height: 300px;
  height: fit-content;
}
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
.card{
     background-color:rgb(33, 33, 33);
     color:white;
     border-radius: 18px;
}
.card-img-top{
     padding:10px;
     border-radius: 8px;
}
ul li{
     padding: 20px;
}
</style>