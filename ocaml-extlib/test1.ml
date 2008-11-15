module StringMap = Map.Make (String)

let () =
  let map = StringMap.empty in
  let map = StringMap.add "foo" "bar" map in
  let map = StringMap.add "bar" "baz" map in
  let map = StringMap.add "baz" "bil" map in
  let map = StringMap.add "bil" "biz" map in
  print_endline (Std.dump map)

