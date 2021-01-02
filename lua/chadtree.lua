local on_exit = function (_, code)
  vim.api.nvim_err_writeln("CHADTree EXITED - " .. code)
end

local on_stdout = function (_, msg)
  vim.api.nvim_out_write(table.concat(msg, "\n"))
end

local on_stderr = function (_, msg)
  vim.api.nvim_err_write(table.concat(msg, "\n"))
end


local py_main = function ()
  local filepath = "/lua/chadtree.lua"
  local src = debug.getinfo(1).source
  local top_lv = string.sub(src, 2, #src - #filepath)

  local unix = top_lv .. [[/main.py]]
  local windows = top_lv .. [[\main.py]]
  return vim.fn.filereadable(unix) and unix or windows
end


local main = py_main()
local args = { "python3", main, vim.fn.serverstart() }
vim.fn.jobstart(args, { on_exit = on_exit, on_stdout = on_stdout, on_stderr = on_stderr })