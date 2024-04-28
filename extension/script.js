const processedUserIds = new Set();

function getHaqScore(userid) {
  console.log("New tweet detected! UserID:", userid);
  if (userid == "fnerrise") {
    // Pre determined HaQ Score for a specific user
    return 97;
  } else if (userid == "elonmusk") {
    // Pre determined HaQ Score for a specific user
    return 88;
  } else {
    // Mock HaQ Score for all other users, it would be replaced with Twitter's API
    return Math.floor(Math.random() * 56) + 40;
    // return Math.floor(Math.random() * 100);
  }
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

function checkForNewTweets() {
  console.log("Checking for new tweets...");
  const spansWithAtSymbol = document.querySelectorAll("span");

  spansWithAtSymbol.forEach((tweetHandle) => {
    if (
      processedUserIds.has(tweetHandle) ||
      !tweetHandle.innerText.includes("@")
    ) {
      return;
    } else {
      const score = getHaqScore(tweetHandle.innerText.slice(1));
      processedUserIds.add(tweetHandle, score);
      addScoreToDOM(tweetHandle, score);
    }
  });
}

// Set an interval to check for new tweets every second
setInterval(checkForNewTweets, 1000);
