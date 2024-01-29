document.getElementById('search-form').addEventListener('submit', function(event) {
			event.preventDefault(); // Prevent the default form submission behavior
			var xhr = new XMLHttpRequest();
		 

			// Get the selected checkbox value
			var checkboxCategory = document.getElementById('category').value;

			// Get the user input subcategory
			var userInputSubcategory = document.getElementById('user-input-subcategory').value;

			// Construct the desired URL
			var url = `https://cs2300.skrublaub.xyz/api/search_html/${checkboxCategory}/?search_term=${userInputSubcategory}`;
						
			// Send the request to the server
			xhr.open('GET', url, true);
			xhr.onreadystatechange = function() {
				if (xhr.readyState === 4 && xhr.status === 200) {
					document.getElementById('display-html').innerHTML = xhr.responseText;
				}
			};
			xhr.send();
			

});
