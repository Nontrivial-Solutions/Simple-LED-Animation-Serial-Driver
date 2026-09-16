#https://ziap.github.io/blog/nixos-cross-compilation/
{
  description = "Flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    {

      devShells.${system}.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          act
          codespell
          cppcheck
          just
          prettier
          prek
          rip2
          ruff
          tombi
          uv
          wget
          rumdl
        ];

        TODO_DIR = "./.todo/";

        shellHook = ''
          prek install -f
          just bootstrap
          source .venv/bin/activate
          echo done!
        '';
      };
    };
}