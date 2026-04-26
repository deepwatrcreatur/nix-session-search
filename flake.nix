{
  description = "Nix-packaged session history indexing and search for agent workflows";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = f:
        nixpkgs.lib.genAttrs systems (system:
          f {
            pkgs = import nixpkgs { inherit system; };
          });
    in
    {
      formatter = forAllSystems ({ pkgs }: pkgs.nixfmt-rfc-style);

      packages = forAllSystems ({ pkgs }: {
        cass = pkgs.callPackage ./pkgs/cass.nix { };
        default = self.packages.${pkgs.system}.cass;
      });

      devShells = forAllSystems ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            jq
            nixfmt-rfc-style
            python3
            sqlite
          ];
        };
      });
    };
}
