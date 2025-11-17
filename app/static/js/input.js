

function InsertString(Self, Str)
{
	let Start = Self.selectionStart;
	let End = Self.selectionEnd;

	// set textarea value to: text before caret + tab + text after caret
	Self.value = Self.value.substring(0, Start) + Str + Self.value.substring(End);

	// put caret at right position again
	Self.selectionStart = Self.selectionEnd = Start + Str.length;
}

function EnableTabInputForTextArea()
{
	let TextAreas = document.getElementsByTagName('textarea');
	for (let i = 0; i < TextAreas.length; i++)
	{
		TextAreas[i].addEventListener("keydown", function(e) {
			if (e.key == "Tab") 
			{
				e.preventDefault();
				InsertString(this, "\t");
			}
		});
	}
}
EnableTabInputForTextArea();

