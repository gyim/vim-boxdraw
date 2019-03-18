let s:drawscript = expand('<sfile>:p:h:h') . "/python/boxdraw.py"

function! boxdraw#GetEndPos()
	" Vim reports '< and '> in the wrong order if the end of the selection
	" is in an earlier line than the start of the selection. This is why
	" we need this hack.
	let m = getpos("'m")
	execute "normal! gvmm\<Esc>"
	let p = getpos("'m")
	call setpos("'m", m)
	return p
endfunction

function! boxdraw#GetStartPos(startPos)
	" Returns the 'other corner' of the visual selection.
	let p1 = getpos("'<")
	let p2 = getpos("'>")
	if p1 == a:startPos
		return p2
	else
		return p1
	endif
endfunction

function! boxdraw#Draw(cmd, args)
	let p2 = boxdraw#GetEndPos()
	let p1 = boxdraw#GetStartPos(p2)
	let y1 = p1[1] - 1
	let y2 = p2[1] - 1
	let x1 = p1[2] + p1[3] - 1
	let x2 = p2[2] + p2[3] - 1
	let c = ['python', s:drawscript, shellescape(a:cmd), y1, x1, y2, x2] + a:args
	execute "%!" . join(c, " ")
	call setpos(".", p2)
endfunction

function! boxdraw#DrawWithLabel(cmd, args)
	let label = shellescape(input("Label: "))
	call boxdraw#Draw(a:cmd, [label] + a:args)
endfunction

function! boxdraw#Select(cmd)
	let p2 = boxdraw#GetEndPos()
	let p1 = boxdraw#GetStartPos(p2)
	let y1 = p1[1] - 1
	let y2 = p2[1] - 1
	let x1 = p1[2] + p1[3] - 1
	let x2 = p2[2] + p2[3] - 1

	let contents = join(getline(1,'$'), "\n")
	let c = ['python', s:drawscript, shellescape(a:cmd), y1, x1, y2, x2]
	let result = system(join(c, " "), contents)

	let coords = split(result, ",")
	
	call setpos("'<", [0, coords[0]+1, coords[1]+1, 0])
	call setpos("'>", [0, coords[2]+1, coords[3]+1, 0])
	normal! gv
endfunction

function! boxdraw#debug()
	echo "debug"
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
vnoremap +v :<C-u>call boxdraw#Draw("+v", [])<CR>
vnoremap +V :<C-u>call boxdraw#Draw("+v", [])<CR>
vnoremap +^ :<C-u>call boxdraw#Draw("+^", [])<CR>

vnoremap ++> :<C-u>call boxdraw#Draw("++>", [])<CR>
vnoremap ++< :<C-u>call boxdraw#Draw("++<", [])<CR>
vnoremap ++v :<C-u>call boxdraw#Draw("++v", [])<CR>
vnoremap ++V :<C-u>call boxdraw#Draw("++v", [])<CR>
vnoremap ++^ :<C-u>call boxdraw#Draw("++^", [])<CR>

vnoremap +- :<C-u>call boxdraw#Draw("+-", [])<CR>
vnoremap +_ :<C-u>call boxdraw#Draw("+_", [])<CR>
vnoremap +\| :<C-u>call boxdraw#Draw("+\|", [])<CR>

" Selection
vnoremap ao :<C-u>call boxdraw#Select("ao")<CR>
vnoremap io :<C-u>call boxdraw#Select("io")<CR>

