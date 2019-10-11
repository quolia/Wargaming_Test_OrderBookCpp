#pragma once
#ifndef _WTEST_UTILS_H
#define _WTEST_UTILS_H

#include <locale>
#include <iostream>
#include <string>
#include <sstream>

using namespace std;

class utils
{
public:

	static wstring widen(const string& str)
	{
		wostringstream wstm;
		const ctype<wchar_t>& ctfacet = use_facet<ctype<wchar_t>>(wstm.getloc());
		for (size_t i = 0; i < str.size(); ++i)
		{
			wstm << ctfacet.widen(str[i]);
		}
		return wstm.str();
	}

	static string narrow(const wstring& str)
	{
		ostringstream stm;
		const ctype<char>& ctfacet = use_facet<ctype<char>>(stm.getloc());
		for (size_t i = 0; i < str.size(); ++i)
		{
			stm << ctfacet.narrow(str[i], 0);
		}
		return stm.str();
	}
};

#endif // _WTEST_UTILS_H