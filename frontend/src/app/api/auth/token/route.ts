import { getAccessToken } from '@auth0/nextjs-auth0';
import { NextResponse } from 'next/server';

export async function GET() {
  try {
    const result = await getAccessToken();
    
    // Get userinfo using the access token
    const userInfoResponse = await fetch(`https://${process.env.AUTH0_DOMAIN}/userinfo`, {
      headers: {
        Authorization: `Bearer ${result.accessToken}`
      }
    });

    if (!userInfoResponse.ok) {
      throw new Error('Failed to fetch user info');
    }

    const userInfo = await userInfoResponse.json();
    
    console.log('Token request result:', {
      accessToken: result.accessToken ? 'present' : 'missing',
      userInfo: userInfo
    });
    
    return NextResponse.json({ 
      accessToken: result.accessToken,
      userInfo 
    });
  } catch (error) {
    console.error('Failed to get access token or user info:', error);
    return new NextResponse(
      JSON.stringify({ error: 'Failed to get access token or user info' }),
      { status: 401 }
    );
  }
} 