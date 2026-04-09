{
  lib,
  fetchFromGitHub,
  rustPlatform,
  pkg-config,
  openssl,
  sqlite,
  installShellFiles,
  versionCheckHook,
  onnxruntime,
  stdenv,
}:

rustPlatform.buildRustPackage rec {
  pname = "cass";
  version = "0.1.63";

  src = fetchFromGitHub {
    owner = "Dicklesworthstone";
    repo = "coding_agent_session_search";
    rev = "v${version}";
    hash = "sha256-o4crQ4KhCdQDSG5puVCnd3CCdIhaNWZVj2BQygI87ho=";
  };

  cargoHash = "sha256-ies7oUyYMqIfBn3etoRdbdu63H71/n1+VbL7WLktqYA=";

  # Disable slow LTO settings for faster builds
  # Remove lld linker override - it breaks rpath setting in Nix
  postPatch = ''
    substituteInPlace Cargo.toml \
      --replace-fail 'lto = true' 'lto = false' \
      --replace-fail 'codegen-units = 1' ""
    rm -f .cargo/config.toml
  '';

  nativeBuildInputs = [
    pkg-config
    installShellFiles
  ];

  buildInputs = [
    openssl
    sqlite
    onnxruntime
  ];

  # Point ort-sys to nixpkgs onnxruntime
  preBuild = ''
    export ORT_SKIP_DOWNLOAD=1
    export ORT_LIB_LOCATION=${onnxruntime}/lib
    export ORT_PREFER_DYNAMIC_LINK=1
  '';

  # The main binary is cass
  cargoBuildFlags = [
    "--bin"
    "cass"
  ];

  # Tests require a writable HOME directory
  doCheck = false;

  postInstall = lib.optionalString (stdenv.buildPlatform.canExecute stdenv.hostPlatform) ''
    # Generate shell completions
    $out/bin/cass completions bash > cass.bash && installShellCompletion --bash cass.bash
    $out/bin/cass completions fish > cass.fish && installShellCompletion --fish cass.fish
    $out/bin/cass completions zsh > cass.zsh && installShellCompletion --zsh cass.zsh

    # Generate man page
    $out/bin/cass man > cass.1
    installManPage cass.1
  '';

  # versionCheckHook might not be available in all nixpkgs versions
  # doInstallCheck = true;
  # nativeInstallCheckInputs = [ versionCheckHook ];

  meta = with lib; {
    description = "Unified, high-performance TUI to index and search your local coding agent history";
    homepage = "https://github.com/Dicklesworthstone/coding_agent_session_search";
    license = licenses.mit;
    platforms = platforms.linux;
    mainProgram = "cass";
  };
}
