(* Test the Format module, which we suspect may not be working. *)

open Format

let debug = false

let () =
  if debug then Printf.printf "creating buffer ...\n%!";
  let buf = Buffer.create 100 in
  if debug then Printf.printf "creating formatter ...\n%!";
  let fmt = formatter_of_buffer buf in
  if debug then Printf.printf "open box ...\n%!";
  pp_open_box fmt 0;
  if debug then Printf.printf "print string ...\n%!";
  pp_print_string fmt "This is a string";
  if debug then Printf.printf "close box ...\n%!";
  pp_close_box fmt ();
  if debug then Printf.printf "flush ...\n%!";
  pp_print_flush fmt ();
  if debug then Printf.printf "get buffer contents ...\n%!";
  let str = Buffer.contents buf in
  Printf.printf "contents of buffer = %S\n%!" str
