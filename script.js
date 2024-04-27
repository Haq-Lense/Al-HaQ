// Global set to keep track of processed tweet userids to avoid duplication
const processedUserIds = new Set();

// Function to perform an action with the userid
function foo(userid) {
  console.log("New tweet detected! UserID:", userid);
  return Math.floor(Math.random() * 100);
}

function addScoreToDOM(tweet, score) {
  const spanScore = document.createElement("span");
  if (score >= 70) {
    spanScore.style.color = "green";
  } else if (score >= 40) {
    spanScore.style.color = "orange";
  } else {
    spanScore.style.color = "red";
  }
  spanScore.style.fontWeight = "bold";
  spanScore.style.marginLeft = "15px";
  spanScore.innerText = "HaQ Score: " + score + "%";
  tweet.appendChild(spanScore);
}

// Function to check for new tweets and call foo() with userid
function checkForNewTweets() {
  console.log("Checking for new tweets...");
  const spansWithAtSymbol = document.querySelectorAll("span");

  spansWithAtSymbol.forEach((tweetHandle) => {
    if (
      !processedUserIds.has(tweetHandle) &&
      tweetHandle.innerText.includes("@")
    ) {
      const score = foo(tweetHandle.innerText.slice(1));
      processedUserIds.add(tweetHandle, score);
      addScoreToDOM(tweetHandle, score);
    }
  });
}

// Set an interval to check for new tweets every second (adjust interval as needed)
setInterval(checkForNewTweets, 1000);
