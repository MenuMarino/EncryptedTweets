function submit_entry(){
    var user = document.getElementById('name');
    var tweet = document.getElementById('tweet');

    var entry = {
      user: user.value,
      tweet: tweet.value
    };


    console.log(entry);
  }