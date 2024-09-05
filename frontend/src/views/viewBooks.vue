<script setup>
import router from '@/router';
import {ref,onMounted} from 'vue'
const booksData=ref([[{
     'Bid':0,
     'Name':'BookName',
     'AuthorName':'AuthorName',
     'AvgRating':0,
     'CoverPath':'../assets/book-cover.jpg'
}]])



// convert path


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

// fetch books
async function fetchBooks() {
     const token = localStorage.getItem('token');
     const res= await fetch("http://localhost:8080/api/books",{
          method:"GET",
          headers: {
               'Authorization': `Bearer ${token}`,
               'Content-Type':'application/json'
          }
     });
     if (res.status == 200) {
  let temp = [];
  let temp2 = [];
  let result = await res.json();
  if (result.length > 0) {
    for (let i = 0; i < result.length; i += 2) {
      temp.push(result[i]);
      temp.push(result[i + 1]);
      temp2.push(temp);
      temp = [];
    }

    for (let i = 0; i < temp2.length; i++) {
      for (let j = 0; j < temp2[i].length; j++) {
        if (temp2[i][j]) {
          const element = temp2[i][j];
          element.CoverPath = convertPath(element.CoverPath);
        }
      }
    }

    booksData.value = temp2;
    console.log(booksData.value);
  } else {
    console.log('No books found');
  }
} else if (res.status == 401) {
  localStorage.removeItem('token');
  router.push('/LibrarianLogin');
}

}

// edit book
function editBook(Bid) {
     router.push(`/editBook/${Bid}`);
}

// delete books
async function DeleteBook(Bid){
     const token = localStorage.getItem('token');
     const b={
          "Bid":Bid
     }
     const res= await fetch("http://localhost:8080/api/books",{
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
onMounted(async () => {
     await fetchBooks();
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
          </div>
          <div class="col" style="margin: 10px;">
               
                    <div style="display: flex; justify-content: space-between; align-items: center;margin-bottom: 10px;margin-right: 5px;">
                         <h3 style="color: white;">Books</h3>
                         <button class="btn btn-primary" @click="()=>{router.push('/AddBook')}">Add Book</button>
                    </div>
               <div id="books">
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
                                                  <div>
                                                       <button class="btn btn-danger" @click="DeleteBook(booksData[i-1][0].Bid)" style="margin: 5px;">Delete</button>
                                                       <button class="btn btn-outline-primary"@click="editBook(booksData[i-1][0].Bid)" style="margin: 5px;">Edit</button>
                                                       <button class="btn btn-primary" data-bs-toggle="modal" :data-bs-target="`#book-modal-${booksData[i-1][0].Bid}`" style="margin: 5px;" >View</button>
                                                  </div>
                                                  <div style="backdrop-filter: blur(55px);" class="modal fade" :id="`book-modal-${ booksData[i-1][0].Bid }`" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                                       <div class="modal-dialog">
                                                            <div class="modal-content">
                                                                 <div class="modal-header" style="color: white;background-color:rgb(33, 33, 33);border: 0px;">
                                                                      <h1 class="modal-title fs-5" id="exampleModalLabel">{{ booksData[i-1][0].Name }}</h1>
                                                                      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                                 </div>
                                                                 <div class="modal-body" style="color: white;background-color:rgb(33, 33, 33)">
                                                                      <h3>Author Name:{{ booksData[i-1][0].AuthorName }}</h3>
                                                                      <h3>Content</h3>
                                                                      <p>{{ booksData[i-1][0].Content }}</p>
                                                                 </div>
                                                                 <div class="modal-footer" style="color: white;background-color:rgb(33, 33, 33);border: 0px;">
                                                                      <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                                                 </div>
                                                            </div>
                                                       </div>
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
                                                  <div>
                                                       <button class="btn btn-danger" @click="DeleteBook(booksData[i-1][1].Bid)" style="margin: 5px;">Delete</button>
                                                       <button class="btn btn-outline-primary" @click="editBook(booksData[i-1][1].Bid)" style="margin: 5px;">Edit</button>
                                                       <button class="btn btn-primary" data-bs-toggle="modal" :data-bs-target="`#book-modal-${booksData[i-1][1].Bid}`" style="margin: 5px;" >View</button>
                                                  </div>
                                                  <div style="backdrop-filter: blur(55px);" class="modal fade" :id="`book-modal-${ booksData[i-1][1].Bid }`" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                                       <div class="modal-dialog">
                                                            <div class="modal-content">
                                                                 <div class="modal-header" style="color: white;background-color:rgb(33, 33, 33);border: 0px;">
                                                                      <h1 class="modal-title fs-5" id="exampleModalLabel">{{ booksData[i-1][1].Name }}</h1>
                                                                      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                                 </div>
                                                                 <div class="modal-body" style="color: white;background-color:rgb(33, 33, 33)">
                                                                      <h3>Author Name:{{ booksData[i-1][1].AuthorName }}</h3>
                                                                      <h3>Content</h3>
                                                                      <p>{{ booksData[i-1][1].Content }}</p>
                                                                 </div>
                                                                 <div class="modal-footer" style="color: white;background-color:rgb(33, 33, 33);border: 0px;">
                                                                      <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
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