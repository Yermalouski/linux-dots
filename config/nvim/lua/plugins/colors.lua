return {
  {
    "ellisonleao/gruvbox.nvim",
    opts = {
      transparent_mode = true,
    },
  },

  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "gruvbox",
    },
  },
  {
      "nvim-lualine/lualine.nvim",
      dependencies = {
	  "nvim-tree/nvim-web-devicons",
      },
      opts = {
	  theme = "gruvbox_dark",
      }
  },
}
