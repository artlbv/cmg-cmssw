{
  #include <string>
  string includePath(gSystem->GetIncludePath());
  gSystem->SetIncludePath((includePath+" -I$ROOFITSYS/include").c_str());
  gROOT->ProcessLine(".L TH1Keys.cc++");
}
