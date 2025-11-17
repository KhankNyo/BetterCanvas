
function EnableTabInputForTextArea()
{
	let TextAreas = document.getElementsByTagName('textarea');
	for (let i = 0; i < TextAreas.length; i++)
	{
		TextAreas[i].addEventListener("keydown", function(e) {
			if (e.key == "Tab") {
				e.preventDefault();
				var Start = this.selectionStart;
				var End = this.selectionEnd;

				// set textarea value to: text before caret + tab + text after caret
				this.value = this.value.substring(0, Start) + "    " + this.value.substring(End);

				// put caret at right position again
				this.selectionStart = this.selectionEnd = Start + 1;
			}
		});
	}
}
EnableTabInputForTextArea();

