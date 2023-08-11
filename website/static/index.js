

function like(postId) { /* Defines the function with the parameter of postId */
  const likeCount = document.getElementById(`likes-count-${postId}`); /* Displays the count of likes */
  const likeButton = document.getElementById(`like-button-${postId}`); /* Displays the button to like a post */

  fetch(`/like-post/${postId}`, { method: "POST" }) /* Registers a like */
    .then((res) => res.json()) /* Converts the response into json */
    .then((data) => { /* Updates the html to display the new like responsively */
      likeCount.innerHTML = data["likes"]; 
      if (data["liked"] === true) { /* Checks if the post is liked by the user */
        likeButton.className = "fas fa-thumbs-up"; /* Represents the thumbs up icon */
      } else { 
        likeButton.className = "far fa-thumbs-up"; /* Outlines the icon to show it hasnt been like */
      }
    })
    .catch((e) => alert("Could not like post.")); /* If an error occurs return an error message */
}
