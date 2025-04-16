import { Github, Twitter, Mail, Linkedin } from "lucide-react"
import { useTheme } from "@/theme/theme"

export default function Footer() {
  const theme = useTheme();

  // Define styles based on theme
  const footerStyle = {
    backgroundColor: theme.colors.cream,
    borderTopColor: theme.colors.lightBlue,
  };

  const headingStyle = {
    ...theme.components.text.heading,
    fontSize: '1.125rem', // text-lg equivalent
  };

  const subheadingStyle = {
    ...theme.components.text.heading,
    fontSize: '1rem', // text-base equivalent
    marginBottom: '0.75rem', // mb-3 equivalent
  };

  const textStyle = {
    ...theme.components.text.body,
    fontSize: '0.875rem', // text-sm equivalent
  };

  const mutedTextStyle = {
    ...theme.components.text.small,
    color: theme.colors.mediumBlue,
  };

  const linkStyle = {
    color: theme.colors.mediumBlue,
    transition: 'color 0.3s ease',
  };

  const linkHoverStyle = {
    color: theme.colors.darkGray,
  };

  return (
    <footer style={{...footerStyle, borderTopWidth: '1px', borderTopStyle: 'solid'}}>
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-3">
            <h3 style={headingStyle}>Algorithm Explorer</h3>
            <p style={mutedTextStyle}>
              Explore and implement various optimization algorithms for your computational problems.
            </p>
          </div>

          <div>
            <h4 style={subheadingStyle}>Resources</h4>
            <ul className="space-y-2">
              {['Documentation', 'API Reference', 'Tutorials', 'Examples'].map((item) => (
                <li key={item}>
                  <a 
                    href="#" 
                    style={linkStyle}
                    onMouseOver={(e) => {
                      e.currentTarget.style.color = linkHoverStyle.color;
                    }}
                    onMouseOut={(e) => {
                      e.currentTarget.style.color = linkStyle.color;
                    }}
                  >
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 style={subheadingStyle}>Company</h4>
            <ul className="space-y-2">
              {['About Us', 'Careers', 'Blog', 'Privacy Policy'].map((item) => (
                <li key={item}>
                  <a 
                    href="#" 
                    style={linkStyle}
                    onMouseOver={(e) => {
                      e.currentTarget.style.color = linkHoverStyle.color;
                    }}
                    onMouseOut={(e) => {
                      e.currentTarget.style.color = linkStyle.color;
                    }}
                  >
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 style={subheadingStyle}>Connect</h4>
            <div className="flex space-x-3">
              {[
                { Icon: Github, label: "GitHub" },
                { Icon: Twitter, label: "Twitter" },
                { Icon: Linkedin, label: "LinkedIn" },
                { Icon: Mail, label: "Email" }
              ].map(({ Icon, label }) => (
                <a
                  key={label}
                  href="#"
                  style={linkStyle}
                  onMouseOver={(e) => {
                    e.currentTarget.style.color = linkHoverStyle.color;
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.color = linkStyle.color;
                  }}
                  aria-label={label}
                >
                  <Icon className="h-5 w-5" />
                </a>
              ))}
            </div>
            <div className="mt-4">
              <p style={mutedTextStyle}>
                Have questions?{" "}
                <a 
                  href="#" 
                  style={{
                    color: theme.colors.darkGray,
                    fontWeight: 'bold',
                  }}
                  onMouseOver={(e) => {
                    e.currentTarget.style.textDecoration = 'underline';
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.textDecoration = 'none';
                  }}
                >
                  Contact Support
                </a>
              </p>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t flex flex-col md:flex-row justify-between items-center" style={{ borderTopColor: theme.colors.lightBlue }}>
          <p style={mutedTextStyle}>
            © {new Date().getFullYear()} Algorithm Explorer. All rights reserved.
          </p>
          <div className="mt-4 md:mt-0 flex space-x-4">
            {['Terms of Service', 'Privacy Policy', 'Cookie Policy'].map((item) => (
              <a 
                key={item}
                href="#" 
                style={linkStyle}
                onMouseOver={(e) => {
                  e.currentTarget.style.color = linkHoverStyle.color;
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.color = linkStyle.color;
                }}
              >
                {item}
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  )
}
