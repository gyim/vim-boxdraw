let s:drawscript = expand('<sfile>:p:h:h') . "/python/boxdraw.py"

function boxdraw#Draw(cmd, args)
	let p1 = getpos("'<")
	let p2 = getpos("'>")
	let y1 = p1[1] - 1
	let y2 = p2[1] - 1
	let x1 = p1[2] + p1[3] - 1
	let x2 = p2[2] + p2[3] - 1
	let c = [s:drawscript, shellescape(a:cmd), y1, x1, y2, x2] + a:args
	execute "%!" . join(c, " ")
	call setpos(".", p2)
endfunction

function boxdraw#DrawWithLabel(cmd, args)
	let label = shellescape(input("Label: "))
	call boxdraw#Draw(a:cmd, [label] + a:args)
endfunction

function boxdraw#DrawConnection()
	let p2 = getpos("'>")
	call boxdraw#Draw("++", [])
	call setpos("'<", p2)
	execute "normal! gv"
endfunction

function boxdraw#debug()
	echo s:drawscript
endfunction

" -------- Keyboard mappings --------

" Box drawing
vnoremap +o :<C-u>call boxdraw#Draw("+o", [])<CR>
vnoremap +O :<C-u>call boxdraw#DrawWithLabel("+O", [])<CR>
vnoremap +[O :<C-u>call boxdraw#DrawWithLabel("+[O", [])<CR>
vnoremap +]O :<C-u>call boxdraw#DrawWithLabel("+]O", [])<CR>
vnoremap +{[O :<C-u>call boxdraw#DrawWithLabel("+{[O", [])<CR>
vnoremap +{]O :<C-u>call boxdraw#DrawWithLabel("+{]O", [])<CR>
vnoremap +}[O :<C-u>call boxdraw#DrawWithLabel("+}[O", [])<CR>
vnoremap +}]O :<C-u>call boxdraw#DrawWithLabel("+}]O", [])<CR>

" Labeling
vnoremap +c :<C-u>call boxdraw#DrawWithLabel("+c", [])<CR>
vnoremap +{c :<C-u>call boxdraw#DrawWithLabel("+{c", [])<CR>
vnoremap +}c :<C-u>call boxdraw#DrawWithLabel("+}c", [])<CR>
vnoremap +{[c :<C-u>call boxdraw#DrawWithLabel("+{[c", [])<CR>
vnoremap +{]c :<C-u>call boxdraw#DrawWithLabel("+{]c", [])<CR>
vnoremap +}[c :<C-u>call boxdraw#DrawWithLabel("+}[c", [])<CR>
vnoremap +}]c :<C-u>call boxdraw#DrawWithLabel("+}]c", [])<CR>
vnoremap +[c :<C-u>call boxdraw#DrawWithLabel("+[c", [])<CR>
vnoremap +]c :<C-u>call boxdraw#DrawWithLabel("+]c", [])<CR>
vnoremap +D :<C-u>echo boxdraw#debug()<CR>

" Line drawing
vnoremap +> :<C-u>call boxdraw#Draw("+>", [])<CR>
vnoremap +< :<C-u>call boxdraw#Draw("+<", [])<CR>
vnoremap +: :<C-u>call boxdraw#Draw("+:", [])<CR>
vnoremap ++ :<C-u>call boxdraw#DrawConnection()<CR>

